# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dogwalker.db')
DATABASE_CONNECT_OPTIONS = {}
OPENAPI_VERSION = '3.0.3'
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

OPENAPI_REDOC_PATH = '/redoc'
OPENAPI_URL_PREFIX = '/doc'
OPENAPI_JSON_PATH = 'openapi.json'
OPENAPI_SWAGGER_UI_PATH = '/swagger'
OPENAPI_SWAGGER_UI_VERSION = '3.18.3'
OPENAPI_SWAGGER_UI_SUPPORTED_SUBMIT_METHODS = ['get']
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "987654321987"

# Secret key for signing cookies
SECRET_KEY = "123456789123"

SECURITY_PASSWORD_SALT = "MY_SALT"