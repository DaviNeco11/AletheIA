from dotenv import load_dotenv
import os

load_dotenv()  # carrega automaticamente o .env no mesmo diretório

print(os.getenv("USER_NAME"))
print(os.getenv("APP_MODE"))
print(os.getenv("SECRET_KEY"))
