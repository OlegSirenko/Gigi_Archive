import time
import random
import vk
from database_afishe import set_group, get_groups
from BotTG import send_photo_to_vk

token = ""


def download_image(url):
    from PIL import Image
    import requests

    im = Image.open(requests.get(url, stream=True).raw)
    im.save("/home/tehnokrat/PythonProjects/Posters/poster_from_group.jpg")


def check_post(info, group):
    if group[2]:  # group[2] is last_post_id, if group initialized =>
        post_id = info['items'][0]['id']
        if not post_id == group[2]:  # check do we have new post, if post != post_in_db => new post
            print(f'In group {group[1]} new post, checking attachments')
            dice = random.randint(0, 99)
            if group[1] == "baneks" and 7 == dice:
                if 'attachments' in info['items'][0]:
                    post_text = "ВАУ ЧТО ЭТО? ЭТО АВТОМАТИЗИРОВАННАЯ ПАСХАЛКА? У НЕЕ ЖЕ ШАНС 1 ИЗ 100! \n(From Анекдоты категории Б)\n\n" + info['items'][0]['copy_hystory'][0]['text']
                    photo_url = info['items'][0]['copy_hystory'][0]['attachments'][0]['photo']['sizes'][-1]['url']
                    print(post_text, post_id)
                    download_image(photo_url)
                    set_group(group_id=group[0], domain=group[1], last_post_id=post_id, post_text=post_text,
                              photo_attachments_url=photo_url)
                    return
                else:    
                    post_text = "ВАУ ЧТО ЭТО? ЭТО АВТОМАТИЗИРОВАННАЯ ПАСХАЛКА? У НЕЕ ЖЕ ШАНС 1 ИЗ 100! \n(From Анекдоты категории Б)\n\n" + info['items'][0]['text']
                    print(post_text)
                    set_group(group_id=group[0], domain=group[1], last_post_id=post_id, post_text=post_text)
                    return
            elif group[1] == "baneks":
                print(f"Not Lucky((( Random int == {dice}")
                set_group(group_id=group[0], domain=group[1], last_post_id=post_id, post_text=None, is_published=True)
                return
            print(f'Just checked {group[1]} is it easter egg, it is not')
            if 'copy_history' in info['items'][0]:  # check if post from other group
                print("There is 'copy_text'")
                post_text = f"#афиша\n(From https://vk.com/{group[1]}\n\n" + str(info['items'][0]['copy_history'][0]['text'])
                photo_url = info['items'][0]['copy_history'][0]['attachments'][0]['photo']['sizes'][-1]['url']
                #print(post_text, post_id)
                download_image(photo_url)
                set_group(group_id=group[0], domain=group[1], last_post_id=post_id, post_text=post_text,
                          photo_attachments_url=photo_url)
                send_photo_to_vk(caption=post_text, source="group_vk")
            elif 'attachments' in info['items'][0]:
                post_text = f"#афиша\n(From https://vk.com/{group[1]}\n\n" + str(info['items'][0]['text'])
                photo_url = info['items'][0]["attachments"][0]['photo']['sizes'][-1]['url']
                print(post_id, post_text)
                download_image(photo_url)
                set_group(group_id=group[0], domain=group[1], last_post_id=post_id, post_text=post_text,
                          photo_attachments_url=photo_url)
                send_photo_to_vk(caption=post_text, source="group_vk")
    else:
        print("initializing")
        post_id = info['items'][0]['id']
        set_group(group[0], group[1], post_id)


def get_post(group):
    info = vk_api.wall.get(access_token=token, owner_id=group[0], domein=group[1], offset=0, count=1, v=5.131)
    time.sleep(0.4)
    if ("is_pinned" in info['items'][0]) and int(info['items'][0]['is_pinned']):
        info = vk_api.wall.get(access_token=token, owner_id=group[0], domein=group[1], offset=1, count=1, v=5.131)
        print(f"{group[1]} has pinned post and last post_id = {info['items'][0]['id']}")
        check_post(info, group)
    elif not 'is_pinned' in info['items'][0]:
        check_post(info, group)
    time.sleep(0.4)


def main():
    while True:
        groups = get_groups()
        if groups:
            try:
                for group in groups:
                    if group[0]:
                        print(group)
                        get_post(group=group)
            except Exception as e:
                print(e)
        time.sleep(3)


if __name__ == "__main__":
    session = vk.Session(access_token=token)  # Авторизация
    vk_api = vk.API(session)
    main()
