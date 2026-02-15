import os
import dropbox
from dotenv import load_dotenv

def upload_to_dropbox_seq(text, bn=None, dr=None, file_extension=".txt"):

  # Get the access token from the environment variable
  DROPBOX_TOKEN = os.environ['DROPBOX_TOKEN']

  # If bn or dr are not provided, try to get them from environment variables
  if bn is None:
    bn = os.getenv('BN')
    if bn is None:
      load_dotenv()
      bn = os.getenv('BN')
    print(f"bn: {bn}")

  if dr is None:
    dr = os.getenv('DR')
    if dr is None:
      load_dotenv()
      dr = os.getenv('DR')
    print(f"dr: {dr}")

  # Create a Dropbox client object
  client = dropbox.Dropbox(DROPBOX_TOKEN)

  # Create a new file with the given name in the specified directory
  seq=1
  #pad the seq
  seq_str = str(seq).zfill(3)
  file_name = f"{dr}/{bn}-{seq_str}{file_extension}"
  
  # Check if the file already exists
  while True:
    try:
      client.files_get_metadata(file_name)
      seq += 1
      seq_str = str(seq).zfill(3)
      file_name = f"{dr}/{bn}-{seq_str}{file_extension}"
    except dropbox.exceptions.ApiError:
      break
  client.files_upload(text.encode('utf-8'), file_name)

  print(f"File {file_name} saved successfully!")

os.environ['BN'] = 'bypythonista'

os.environ['DR'] = '/ART/CeSaReT/tmp'
# Example usage
upload_to_dropbox_seq("Hello, World!  from pyrhonista")
