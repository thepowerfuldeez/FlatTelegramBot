import vk_api
import os

vk_session = vk_api.VkApi(token=os.environ.get("VK_TOKEN"))
vk = vk_session.get_api()


def get_public_updates(public_id, n=20, offset=0):
    try:
        posts = vk.wall.get(owner_id=-public_id, count=n, offset=offset, v=5.71)
        return posts['items']
    except:
        return []
