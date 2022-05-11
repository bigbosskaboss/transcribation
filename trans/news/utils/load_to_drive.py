import os

from django.conf import settings

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()


def upload_file(file_path='', file_name=''):
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = str(settings.BASE_DIR / 'news/utils/client_secrets.json')
    gauth.LoadCredentialsFile(str(settings.BASE_DIR / 'news/utils/creds.txt'))
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("news/utils/creds.txt")

    drive = GoogleDrive(gauth)
    doc = drive.CreateFile({'title': f'{file_name}'})
    doc.SetContentFile(os.path.join(file_path, file_name))
    doc.Upload()
    return f"https://docs.google.com/document/d/{doc['id']}/edit"
