import vk_api
import database_afishe as db
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests

token = 'vk1.a.8xF0BGNFUDemLCp3f3lLPb6cTqy6WCDW59Dd3vCHvYxWin1Pk-Jtj-KxDef_A6vDxA2ioXBBsYYEp0NIr5mjwXuavALe-n2RR1jChJ1GRWdxYP5PAIZ6sQ3sR4C-0hX2-UCri-oycrIK-Yxp3ReWzrtztKTyhphtafEP8_5s56JgB3DdZD-6R8gk6b_CF8N2'
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, 189400359)
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
            if event.from_chat:
                text = event.message['text']
                if "#афиша" in text:
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
