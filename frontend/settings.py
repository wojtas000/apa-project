import os

BASE_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')
HEADERS = {
    'api-key': os.getenv('API_KEY', '1234567890')
}
