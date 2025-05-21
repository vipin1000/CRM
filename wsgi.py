import os
import sys

# Add the CRM directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'CRM'))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CRM.settings')

# Import the WSGI application
from CRM.wsgi import application 