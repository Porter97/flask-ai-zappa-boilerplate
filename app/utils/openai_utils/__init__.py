from flask import current_app
from retry import retry

from app.utils.openai_utils.prompts import SYSTEM_TRANSLATOR_PROMPT, SYSTEM_CHAT_PROMPT

import enum
import openai
import tiktoken


class SplitType(enum.Enum):
    CHARS = 'chars'
    WORDS = 'words'
    TOKENS = 'tokens'


class OpenAISession:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OpenAISession, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.api_key = self.fetch_api_key()
        self.tokenizer = self.init_tokenizer()
        self.MAX_TOKENS = 4096
        self.init_openai()

    @staticmethod
    def fetch_api_key():
        api_key = current_app.config.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError('OPENAI_API_KEY not found in app configuration')
        return api_key

    def init_openai(self):
        openai.api_key = self.api_key

    @staticmethod
    def init_tokenizer():
        return tiktoken.get_encoding('p50k_base')

    @staticmethod
    def validate_text(text):
        if not isinstance(text, str):
            raise ValueError('Text must be a string')
        if not text:
            raise ValueError('Text cannot be empty')

    def count_tokens(self, text, disallowed_special=()):
        self.validate_text(text)
        tokens = self.tokenizer.encode(text, disallowed_special=disallowed_special)
        return len(tokens)

    def split_text(self, text, overlap, split_type=SplitType.TOKENS, max_length=1024):
        """
        Text should preferably be split into chunks of 256/512 tokens for best results
        """
        self.validate_text(text)
        if not isinstance(max_length, int) or max_length <= 0:
            raise ValueError('max_length must be a positive integer')
        if not isinstance(overlap, int) or overlap <= 0 or overlap >= max_length:
            raise ValueError('overlap must be a positive integer and less than max_length')
        if not isinstance(split_type, SplitType):
            raise ValueError('split_type must be an instance of SplitType')

        chunks = []
        start = 0

        if split_type == SplitType.TOKENS:
            data = self.tokenizer.encode(text, disallowed_special=())
        else:
            raise ValueError('split_type not recognized')

        while start < len(data):
            end = start + max_length
            if end >= len(data):
                end = len(data)
            chunk = ''.join(self.tokenizer.decode([token]) for token in data[start:end])
            chunks.append(chunk)
            start = end - overlap if end < len(data) else end
        return chunks

    @retry(tries=5, delay=1, backoff=2, max_delay=32)
    def generate_embeddings(self, text):
        self.validate_text(text)
        try:
            return openai.Embedding.create(
                input=text,
                model="text-embedding-ada-002"
            )['data'][0]['embedding']
        except Exception as e:
            raise ValueError("Error generating embeddings: ", e)

    @retry(tries=5, delay=1, backoff=2, max_delay=32)
    def translate_to_semantic_query(self, query, max_tokens=250, temperature=0.2, model="gpt-3.5-turbo"):
        """
        Translates a provided query into a semantic query that is more likely to return relevant text snippets
        """
        self.validate_text(query)

        try:
            return openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_TRANSLATOR_PROMPT
                    },
                    {
                        "role": "user",
                        "content":  f"Given the following query, provide a string of text to use in a "
                                    f"semantic query to help get relevant text snippets."
                                    f"INITIAL QUERY: {query} \n"
                                    f"SEMANTIC QUERY: "
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )['choices'][0]['message']['content']
        except Exception as e:
            raise ValueError("Error translating semantic query: ", e)

    @retry(tries=5, delay=1, backoff=2, max_delay=32)
    def generate_chat(self, message, context, max_tokens=500, temperature=0.2, model='gpt-3.5-turbo'):
        """
        Generates a response to a provided message using the given model
        """
        self.validate_text(message)

        try:
            return openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_CHAT_PROMPT + f' CONTEXT: {context} \n'
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )['choices'][0]['message']['content']
        except Exception as e:
            raise ValueError("Error generating chat response: ", e)

