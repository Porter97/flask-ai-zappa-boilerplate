import logging
import os


class EnvironFilter(logging.Filter):
    """Records the application environment (DEV, TEST, PROD) within logs to allow filtering"""
    def filter(self, record):
        record.app_environment = os.environ.get('FLASK_CONFIG', 'DEV')
        return True


LOG_CONFIG = {
    'version': 1,
    'filters': {
        'environ_filter': {
            '()': EnvironFilter
        }
    },
    'formatters': {
        'BASE_FORMAT': {
            'format': '[%(app_environment)s][%(name)s.%(module)s.%(funcName)s:%(lineno)d][%(levelname)s] -- %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
            'formatter': 'BASE_FORMAT',
            'filters': ['environ_filter'],
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.environ.get('LOG_LEVEL', 'DEBUG'),
        },
    }
}

