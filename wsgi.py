import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    app.run() 