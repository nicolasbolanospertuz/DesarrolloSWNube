from celery import Celery
import os
import requests

celery_app = Celery(__name__, broker='redis://localhost:6379/0')
api_url = os.environ.get("API_URL")

@celery_app.task(name="convert_file")
def convert_file(id, original_file_name, new_file_format, token):
    print("Hello Redis")
    """
    request_body = {
        "status": "PROCESSED"
    }
    headers = {
        "Authorization": f'Bearer {token}'
    }
    r = requests.put(f'{api_url}api/tasks/{id}', data=request_body, headers=headers)
    print(f'Response: {r.status_code}')
    """