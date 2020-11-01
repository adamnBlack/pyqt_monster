import requests



headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
url = "https://www.dropbox.com/s/u3fdmdt1dd2f7ep/GMonster.zip?dl=1"
filepath = "test/GMonster.zip"
r = requests.get(url, stream=True, headers=headers)
with open(filepath, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            print(len(chunk))
            f.write(chunk)