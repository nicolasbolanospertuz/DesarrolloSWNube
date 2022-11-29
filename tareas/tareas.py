from celery import Celery
from pydub import AudioSegment
import requests
import os

celery_app = Celery(__name__, broker='redis://127.0.0.1:6379/0')
api_url = 'http://127.0.0.1:5000/'

@celery_app.task(name="convert_file")
def convert_file(id: str, original_file_name: str, new_file_format: str):
    with open('logs.txt', 'a+') as file:
        file.write(f'Tarea del file {id}, nombre file: {original_file_name}\n')
    original_file_info = original_file_name.split(".")
    path = os.path.realpath(__file__)
    dir = os.path.dirname(path)
    dir = dir.replace('tareas', 'files')
    os.chdir(dir)
    with open(original_file_name, mode='rb') as f:
        original_audio = AudioSegment.from_file(f, format=original_file_info[1])
        original_audio.export(f'files/{original_file_info[0]}.{new_file_format}', format=new_file_format)
    url = f'{api_url}api/background/tasks/{id}'
    r = requests.post(url=url)
    print(r.content)
    f.close()