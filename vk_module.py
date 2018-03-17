import vk
import os

vk_session = vk.Session(access_token=os.environ.get("VK_TOKEN"))
vk = vk.API(vk_session)


def get_public_updates(public_id, n=20, offset=0):
    posts = vk.wall.get(owner_id=-public_id, count=n, offset=offset, v=5.71)
    return posts[1:]
