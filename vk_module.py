import vk_api
from config import VK_SERVICE_TOKEN

vk_session = vk_api.VkApi(VK_SERVICE_TOKEN)
vk = vk_session.get_api()


def get_public_updates(public_id):
    try:
        posts = vk.wall.get(-public_id)['items']
    except Exception as e:
        print(e)
        return []
    return posts
