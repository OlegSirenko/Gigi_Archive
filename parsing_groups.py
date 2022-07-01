import time
import vk
from database_afishe import set_group, get_groups
from BotTG import send_photo_to_vk


token = "727895917278959172789591137205b921772787278959110cfb80af35c30e0621e66e2"


def download_image(url):
    from PIL import Image
    import requests

    im = Image.open(requests.get(url, stream=True).raw)
    im.save("/home/tehnokrat/PythonProjects/Posters/poster_from_group.jpg")


def get_post(group, group_id, domain):
    info = vk_api.wall.get(access_token=token, owner_id=group_id, domein=domain, offset=0, count=1, v=5.131)
    time.sleep(0.4)
    if ("is_pinned" in info['items'][0]) and int(info['items'][0]['is_pinned']):
        info = vk_api.wall.get(access_token=token, owner_id=group_id, domein=domain, offset=1, count=1, v=5.131)
        if group[2]:  # group[2] is last_post_id, if group initialized =>
            post_id = info['items'][0]['id']
            if not post_id == group[2]:  # check do we have new post, if post != post_in_db => new post
                if 'attachments' in info['items'][0]:  # if we have poster, we could send message
                    post_text = info['items'][0]['text']
                    photo_url = info['items'][0]["attachments"][0]['photo']['sizes'][-1]['url']
                    print(post_id, post_text)
                    download_image(photo_url)
                    set_group(group_id=group_id, domain=domain, last_post_id=post_id, post_text=post_text,
                              photo_attachments_url=photo_url)
                    send_photo_to_vk(caption=post_text, source="group_vk")
            else:
                print("This is old post")
        else:  # initialize group
            post_id = info['items'][0]['id']
            # print(post_id)
            set_group(group_id, domain, post_id)
    elif not 'is_pinned' in info['items'][0]:
        if group[2]:  # group[2] is last_post_id, if group initialized =>
            post_id = info['items'][0]['id']
            if not post_id == group[2]:  # check do we have new post, if post != post_in_db => new post
                if 'attachments' in info['items'][0]:  # if we have poster, we could send message
                    post_text = info['items'][0]['text']
                    photo_url = info['items'][0]["attachments"][0]['photo']['sizes'][-1]['url']
                    print(post_id, post_text)
                    download_image(photo_url)
                    set_group(group_id=group_id, domain=domain, last_post_id=post_id, post_text=post_text,
                              photo_attachments_url=photo_url)
                    send_photo_to_vk(caption=post_text, source="group_vk")
            else:
                print("This is old post")
        else:  # initialize group
            post_id = info['items'][0]['id']
            # print(post_id)
            set_group(group_id, domain, post_id)
    time.sleep(0.4)


def main():
    while True:
        groups = get_groups()
        try:
            if groups:
                for group in groups:
                    #print(group)
                    get_post(group=group, group_id=group[0], domain=group[1])
        except Exception as e:
            print(e)
        time.sleep(3)


if __name__ == "__main__":
    session = vk.Session(access_token=token)  # Авторизация
    vk_api = vk.API(session)
    main()
