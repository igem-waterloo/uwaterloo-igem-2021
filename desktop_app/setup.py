import os

TARGET = 'placeholder.py'
os.system('pip install -r requirements.txt')
os.system(f'pyinstaller {TARGET} -F -y')
