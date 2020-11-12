# import requests
# from fake_useragent import UserAgent



# headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
# ua = UserAgent()
# userAgent = ua.random
# # headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
# headers = {'user-agent': '{}'.format(userAgent)}
# print(headers)
# url = "https://www.dropbox.com/s/u3fdmdt1dd2f7ep/GMonster.zip?dl=1"
# filepath = "test/GMonster.zip"
# r = requests.get(url, stream=True, headers=headers)
# downloaded = 0
# with open(filepath, 'wb') as f:
#     for chunk in r.iter_content(chunk_size=1024):
#         # print(chunk)
#         if chunk:
#             downloaded+=len(chunk)
#             print("Dowloaded {}".format(downloaded), end='\r')
#             f.write(chunk)
import download_test