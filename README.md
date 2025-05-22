# Online Secure Hospital System

A secure, role-based hospital management system built with Flask, featuring encrypted patient records and digital signatures.

## Features

- Role-based access control (Sysadmin, Receptionist, ChiefDoctor, CuringDoctor, ConsultingDoctor, Patient)
- DES encryption of patient records at rest
- RSA + SHA-256 digital signatures on record updates
- Comprehensive audit logging
- Responsive web interface
- Docker support for easy deployment

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Docker and Docker Compose (optional)

## Quick Start

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd hospital-system
```

2. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the application:
```bash
docker-compose up -d
```

The application will be available at http://localhost:5000

### Manual Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd hospital-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database and generate keys:
```bash
flask init-db
flask generate-keys
```

6. Run the application:
```bash
flask run
```

## Testing

Run the test suite:
```bash
pytest
```

## Project Structure

```
hospital-system/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── views/
│   ├── utils/
│   └── templates/
├── tests/
├── migrations/
├── instance/
├── .env.example
├── config.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Environment Variables

- `FLASK_APP`: Application entry point
- `FLASK_ENV`: Development/Production environment
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: PostgreSQL connection string
- `DES_KEY_PATH`: Path to DES encryption key
- `RSA_PRIVATE_KEY_PATH`: Path to RSA private key
- `RSA_PUBLIC_KEY_PATH`: Path to RSA public key

## Security Features

- All patient records are encrypted at rest using DES
- Every record update is signed using RSA + SHA-256
- Role-based access control for all operations
- Comprehensive audit logging
- CSRF protection on all forms

## API Documentation

API documentation is available at `/api/docs` when running in development mode.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 