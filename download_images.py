import random

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
import io

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
PATH = "sar-dataset/images/val/"

# Obtain your Google credentials
def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    return flow.run_local_server(port=0)

def main():
    # Build the downloader
    creds = get_credentials()
    drive_downloader = build('drive', 'v3', credentials=creds)

    # Replace 'FOLDER_ID' with your actual Google Drive folder ID
    all_folder_ids = [
        '1rzP8J5pBhhgOmWRsfmh-tgAQN6YPAVDc',
        '1muanDVZZIPNbSLxKNd5KP8UliJnRAXHq',
        '1D_LzUbqKXH72fkOc2sTpD2NiOVAl2UJB',
        '1StubobLP43vjT2-BSH3DBzAUDLzMwglp'
    ]

    def get_files_from(folder_id: str) -> list:
        return (drive_downloader
            .files()
            .list(q=f"'{folder_id}' in parents", pageSize=792, orderBy="name")
            .execute()
            .get('files', []))

    all_pics: list[list] = [get_files_from(folder_id) for folder_id in all_folder_ids]

    for file_num in range(1, 792):
        file = random.choice(all_pics)[file_num - 1]
        print("file being downloaded: " + file['name'])
        request = drive_downloader.files().get_media(fileId=file['id'])
        file_io = io.FileIO(PATH + file['name'], 'wb')
        downloader = MediaIoBaseDownload(file_io, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
    print("Download finished...hopefully it worked.")

if __name__ == '__main__':
    main()
