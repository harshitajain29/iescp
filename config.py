from dotenv import load_dotenv
import os
from app import app

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
UPLOAD_FOLDER = 'images'
# Set the absolute path for the upload folder
upload_folder_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)

# Ensure the 'images' folder exists
if not os.path.exists(upload_folder_path):
    os.makedirs(upload_folder_path)

app.config['UPLOAD_FOLDER'] = upload_folder_path