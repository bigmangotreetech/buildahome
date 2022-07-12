# import requests, json
# from flask import jsonify
#
# # url: 'https://fcm.googleapis.com/fcm/send',
# # headers: {
# #     'Content-Type': 'application/json',
# #     'Authorization': 'key=AAAAlQ1Lrfw:APA91bHvI2-qFZNCf-oFfeZgM0JUDxxbuykH_ffka9hPUE0xBpiza4uHF0LmItT_SfMZ1Zl5amGUfAXigaR_VcMsEArqpOwHNup4oRTQ24htJ_GWYH0OWZzFrH2lRY24mnQ-uiHgLyln'
# # },
# # dataType: 'json',
# # contentType: 'application/json',
# # method: "POST",
# # data: JSON.stringify({
# #     'notification': {"title": title.toString(), "body": message.toString()},
# #     "to": "/topics/" + recipient,
# #     "click_action": 'FLUTTER_NOTIFICATION_CLICK'
# #
# # }),
#
#
# recipient = 'Testing1'
# title='Indent rejected'
# message = 'Helllo, how are you doing today'
# url = 'https://fcm.googleapis.com/fcm/send'
# headers = {
#     'Content-Type': 'application/json',
#     'Authorization': 'key=AAAAlQ1Lrfw:APA91bHvI2-qFZNCf-oFfeZgM0JUDxxbuykH_ffka9hPUE0xBpiza4uHF0LmItT_SfMZ1Zl5amGUfAXigaR_VcMsEArqpOwHNup4oRTQ24htJ_GWYH0OWZzFrH2lRY24mnQ-uiHgLyln'
# }
# data = {
#     "notification": {"title": title, "body": message},
#     "to": "/topics/" + recipient,
# }
# response = requests.post(url, headers=headers, data=json.dumps(data))
# print(response.text)

#
# tradesMen = [
#         'Mason',
#         'Helper',
#         'Carpenter',
#         'Barbender',
#         'Painter',
#         'Electrician',
#         'Plumber',
#         'Tile mason',
#         'Granite mason',
#         'Fabricator',
#         'Other workers',
#         'Interior carpenter'
#     ]

# a = '{Carpenter: 6, Barbender: 4}'
# b = a[1:-1].split(',')
# column = 3
# for t in tradesMen:
#     for wm in b:
#         name = wm.split(':')[0]
#         count = wm.split(':')[1]
#         if name.strip() == t:
#             print(t, count)
#     column+=1

