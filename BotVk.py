import vk_api
import database_afishe as db
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests

token = 'vk1.a.QGbRpK0NKY7hOKlf9P4sCDpjKHWxpa9tv6eIZA5Lnr_cjPNv2OIN0VcXSXl232zRrnzlaea6uU9a3MrfDlbnxIwQT_7CEcL23_UsDBiSaAHfRkXBkeBNz7KideSvGm_4slB8zhU_IPv2FzpIsjHI68Lp7_q-0PHTq0uXPnJPyZqQiGCcKgHTvTmcdmRbkYmn'
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, 214304663)
vk_with_api = vk_session.get_api()
    

def download_image(url):
    from PIL import Image
    import requests

    im = Image.open(requests.get(url, stream=True).raw)
    im.save("/home/tehnokrat/PythonProjects/Posters/afisha.jpg")


def main():
    print("Bot Started")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat and (event.chat_id == 4 or event.chat_id == 3):
                text = event.message['text']
                print(event.message)
                if "#афиша" in str(text).lower():
                    if event.message["attachments"]:
                        path = event.message["attachments"][0]
                        if path['type'] == 'wall':
                            download_image(str(path['wall']['attachments'][0]['photo']['sizes'][-1]['url']))
                            text += '\n' + path['wall']['text']
                            file = open("/home/tehnokrat/PythonProjects/url.txt", "w")
                            file.writelines(str(path['wall']['attachments'][0]['photo']['sizes'][-1]['url']))
                            file.close()
                            db.set_poster(source="VK", picture_url=str(path['wall']['attachments'][0]['photo']['sizes'][-1]['url']), text=text)
                        elif path['type'] == 'photo':
                            download_image(str(path['photo']['sizes'][-1]['url']))
                            print(text)
                            file = open("/home/tehnokrat/PythonProjects/url.txt", "w")
                            file.writelines(str(path['photo']['sizes'][-1]['url']))
                            file.close()
                            db.set_poster(source="VK", picture_url=str(path['photo']['sizes'][-1]['url']), text=text)
                print(event.chat_id)


if __name__ == "__main__":
    params = requests.get('https://api.vk.com/method/messages.getLongPollServer',
                      params={'access_token': token, "v": 5.131}).json()['response']
    print(params)
    main()
