import re

from django_mobile.middleware import MobileDetectionMiddleware
from django_mobile import set_flavour
from django.conf import settings


class MobileTabletDetectionMiddleware(MobileDetectionMiddleware):
    # Example how default middleware could be expanded to provide possibility to detect
    # tablet devices.

    user_agents_android_search = u"(?:android)"
    user_agents_mobile_search = u"(?:mobile)"
    user_agents_tablets_search = u"(?:%s)" % u'|'.join(('ipad', 'tablet', ))

    def __init__(self):
        super(MobileTabletDetectionMiddleware, self).__init__()
        self.user_agents_android_search_regex = re.compile(self.user_agents_android_search,
                                                           re.IGNORECASE)
        self.user_agents_mobile_search_regex = re.compile(self.user_agents_mobile_search,
                                                          re.IGNORECASE)
        self.user_agents_tablets_search_regex = re.compile(self.user_agents_tablets_search,
                                                           re.IGNORECASE)

    def process_request(self, request):
        is_tablet = False

        user_agent = request.META.get('HTTP_USER_AGENT')
        if user_agent:
            # Ipad or Blackberry
            if self.user_agents_tablets_search_regex.search(user_agent):
                is_tablet = True
            # Android-device. If User-Agent doesn't contain Mobile, then it's a tablet
            elif (self.user_agents_android_search_regex.search(user_agent) and
                  not self.user_agents_mobile_search_regex.search(user_agent)):
                is_tablet = True
            else:
                # otherwise, let the superclass make decision
                super(MobileTabletDetectionMiddleware, self).process_request(request)

        # set tablet flavour. It can be `mobile`, `tablet` or anything you want
        if is_tablet:
            set_flavour(settings.FLAVOURS[2], request)
