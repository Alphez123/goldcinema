import os
from django.core.wsgi import get_wsgi_application

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')


application = get_wsgi_application()
