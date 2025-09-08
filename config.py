import os

# SUPABASE_SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kl-veda-ird@db.jkddxvhnireuyyhkompp.supabase.co:5432/postgres'
SUPABASE_SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.jkddxvhnireuyyhkompp:kl-veda-ird@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres'


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'kl_research_expo.db')

os.environ.setdefault('DATABASE_URL', SUPABASE_SQLALCHEMY_DATABASE_URI)

if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'development'

# Make sure instance folder exists
if not os.path.exists(INSTANCE_DIR):
    os.makedirs(INSTANCE_DIR)

class Config:
    SITE_URL = "https://kl-research-expo-backend.onrender.com/"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'kl-ird-research-expo-secret-key')

    if os.environ.get('FLASK_ENV') == 'development':
        # Use SQLite for development
        print("Local Database Accessing...")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_PATH
    else:
        print("Using Supabase Database")
        # Use the RENDER_DB_URL for production or deployment
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL',
            SUPABASE_SQLALCHEMY_DATABASE_URI
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False



