import os.path
from aliyunsdkcore.client import AcsClient
from aliyunsdkcdn.request.v20180510.RefreshObjectCachesRequest import RefreshObjectCachesRequest

from .. import settings

def refresh(lists):
    urls = [os.path.join(settings.CDN_BASE_URL, path) for path in lists]
    request = RefreshObjectCachesRequest()
    request.set_accept_format('json')
    request.set_ObjectPath("\n".join(urls))
    AcsClient(settings.ALIYUN_ACCESS_KEY_ID, settings.ALIYUN_ACCESS_KEY_SECRET, "cn-zhangzhou").do_action_with_exception(request)
