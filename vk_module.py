import vk
from config import VK_TOKEN

vk_session = vk.Session(access_token=VK_TOKEN)
vk = vk.API(vk_session)


def get_public_updates(public_id, n=20):
    posts = vk.wall.get(owner_id=-public_id, count=n)
    return posts[1:]


posts = get_public_updates(57466174)
print(len(posts))
print(posts)
