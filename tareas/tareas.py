from celery import Celery
from pydub import AudioSegment
import requests
import os

celery_app = Celery(__name__, broker='redis://127.0.0.1:6379/0')
api_url = 'http://127.0.0.1:5000/'

@celery_app.task(name="convert_file")
def convert_file(id: str, original_file_name: str, new_file_format: str):
    original_file_info = original_file_name.split(".")
    directory = os.path.dirname(__file__)
    rel_path = f'files\{original_file_name}'
    rel_new_path = f'files\{original_file_info[0]}.{new_file_format}'
    abs_path_original = os.path.join(directory, rel_path)
    abs_path_new = os.path.join(directory, rel_new_path)
    original_audio = AudioSegment.from_file(abs_path_original, format=original_file_info[1])
    original_audio.export(abs_path_new, format=new_file_format)
    url = f'{api_url}api/background/tasks/{id}'
    r = requests.post(url=url)
    with open('logs.txt', 'a+') as file:
        file.write(f'{r.content}\n')
    file.close()