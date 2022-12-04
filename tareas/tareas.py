from celery import Celery
from pydub import AudioSegment
from google.cloud import storage
import requests
import os

celery_app = Celery(__name__, broker='redis://127.0.0.1:6379/0')
api_url = os.environ.get("API_INSTANCE_IP")

@celery_app.task(name="convert_file")
def convert_file(id: str, original_file_name: str, new_file_format: str):
    original_file_info = original_file_name.split(".")
    new_file_name = f'{original_file_info}.{new_file_format}'
    bucket = 'nicolas-bolanos-flask-bucket'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(f'files/{original_file_name}')
    blob.download_to_filename(original_file_name)
    original_audio = AudioSegment.from_file(original_file_name, format=original_file_info[1])
    original_audio.export(new_file_name, format=new_file_format)
    blob = bucket.blob(f'files/{new_file_name}')
    blob.upload_from_filename(new_file_name)
    os.remove(original_file_name)
    os.remove(new_file_name)
    url = f'{api_url}api/background/tasks/{id}'
    r = requests.post(url=url)
    with open('logs.txt', 'a+') as file:
        file.write(f'{r.content}\n')
    file.close()