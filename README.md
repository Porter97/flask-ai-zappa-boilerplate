## Flask AI Boilerplate

This repository is meant to be a starting point for creating your own data pipelines and data retrieval API from unstructured data sources such as PDFs and videos. 
The hope is to make starting a new project much easier by giving you a consistent interface and a set of tools that you can use to build your own data retrieval backend.

#### WARNING: This project is still in the early stages of development. It is not yet ready for production use, but feel free to use it as a starting point for your own projects or to contribute to the project.

### Features
This project is built using the following technologies:
- Flask API
- SQLAlchemy ORM
- PostgreSQL database with local SQLite fallback for development
- JWT authentication
- 

### Setup
1. Create a virtual environment and install the requirements
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file and add the following variables:
```
export FLASK_APP=application.py
export FLASK_ENV=development
export FLASK_DEBUG=1
```

3. Run the Flask app
```
flask run
```

### Deployment
This application uses Zappa for deployment. To deploy, run the following command:
```
zappa init
```

Then modify the `zappa_settings.json` file to match your AWS environment. Once you're ready to deploy, run the following command:
```
zappa deploy dev
```
This will deploy the application to AWS Lambda and create the necessary AWS resources. To update the application, run the following command:
```
zappa update dev
```

### Testing
To run the tests, run the following command:
```
python -m unittest discover
```

### Roadmap
- [ ] Add Terraform deployment
- [ ] Add OpenAI GPT-3/GPT-4 integration
- [ ] Add PDF text extraction
- [ ] Add Video transcription
- [ ] Add OpenSearch integration for document search
- [ ] Add AWS integrations for document storage and triggering

### Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

### Links
- Repository:
- Issue tracker:
- Related projects:
- Related articles:
- License:

### References
- [Zappa](https://github.com/Miserlou/Zappa)