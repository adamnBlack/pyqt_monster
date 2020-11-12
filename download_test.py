# import requests

# headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
# url = "https://www.dropbox.com/s/u3fdmdt1dd2f7ep/GMonster.zip?dl=1"
# filepath = "test/GMonster.zip"
# r = requests.get(url, stream=True, headers=headers)
# with open(filepath, 'wb') as f:
#     for chunk in r.iter_content(chunk_size=1024):
#         if chunk:
#             print(len(chunk))
#             f.write(chunk)

# import dropbox
# access_token = "kH6SiiAvB2QAAAAAAAAAAXYHix4lWuvYtjszN6vxaP7cgm5WdJR29QKoIhLJJ8iI"
# dbx = dropbox.Dropbox(access_token)
# print(dbx.users_get_current_account())
# # for entry in dbx.files_list_folder('').entries:
# #     print(entry.name)

# print(dbx.files_get_metadata('/GMonster.zip').size)
# with open("test/GMonster.zip", "wb") as f:
#     metadata, res = dbx.files_download(path="/GMonster.zip")
#     f.write(res.content)


# import requests

# def download_file_from_google_drive(id, destination):
#     URL = "https://docs.google.com/uc?export=download"

#     session = requests.Session()

#     response = session.get(URL, params = { 'id' : id }, stream = True)
#     token = get_confirm_token(response)

#     if token:
#         params = { 'id' : id, 'confirm' : token }
#         response = session.get(URL, params = params, stream = True)

#     save_response_content(response, destination)

# def get_confirm_token(response):
#     for key, value in response.cookies.items():
#         if key.startswith('download_warning'):
#             return value

#     return None

# def save_response_content(response, destination):
#     CHUNK_SIZE = 32768

#     with open(destination, "wb") as f:
#         for chunk in response.iter_content(CHUNK_SIZE):
#             if chunk: # filter out keep-alive new chunks
#                 f.write(chunk)

# if __name__ == "__main__":
#     file_id = '14c3RMn9D-zSFZmsOUB_TTY8jYqe3b5Cx'
#     destination = 'test.zip'
#     download_file_from_google_drive(file_id, destination)

if __name__=='__main__':
    print(__name__)
else:
    print(__name__)