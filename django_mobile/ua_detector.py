import re


class UADetector(object):
    """
    class to detect if an User Agent is a mobile one
    """
    USER_AGENTS_TEST_MATCH = (
        "w3c ", "acs-", "alav", "alca", "amoi", "audi",
        "avan", "benq", "bird", "blac", "blaz", "brew",
        "cell", "cldc", "cmd-", "dang", "doco", "eric",
        "hipt", "inno", "ipaq", "java", "jigs", "kddi",
        "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
        "maui", "maxo", "midp", "mits", "mmef", "mobi",
        "mot-", "moto", "mwbp", "nec-", "newt", "noki",
        "xda",  "palm", "pana", "pant", "phil", "play",
        "port", "prox", "qwap", "sage", "sams", "sany",
        "sch-", "sec-", "send", "seri", "sgh-", "shar",
        "sie-", "siem", "smal", "smar", "sony", "sph-",
        "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
        "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
        "wapi", "wapp", "wapr", "webc", "winw", "xda-",
    )
    USER_AGENTS_TEST_MATCH = r'^(?:%s)' % '|'.join(USER_AGENTS_TEST_MATCH)
    USER_AGENTS_TEST_MATCH_REGEX = re.compile(USER_AGENTS_TEST_MATCH, re.IGNORECASE)

    USER_AGENTS_TEST_SEARCH = u"(?:%s)" % u'|'.join((
        'up.browser', 'up.link', 'mmp', 'symbian', 'smartphone', 'midp',
        'wap', 'phone', 'windows ce', 'pda', 'mobile', 'mini', 'palm',
        'netfront', 'opera mobi',
    ))
    USER_AGENTS_TEST_SEARCH_REGEX = re.compile(USER_AGENTS_TEST_SEARCH, re.IGNORECASE)

    USER_AGENTS_EXCEPTION_SEARCH = u"(?:%s)" % u'|'.join((
        'ipad',
    ))
    USER_AGENTS_EXCEPTION_SEARCH_REGEX = re.compile(USER_AGENTS_EXCEPTION_SEARCH, re.IGNORECASE)

    HTTP_ACCEPT_REGEX = re.compile("application/vnd\.wap\.xhtml\+xml", re.IGNORECASE)

    def __init__(self, request):
        self.request = request

    def is_user_agent_mobile(self):
        is_mobile = False

        if self.request.META.has_key('HTTP_USER_AGENT'):
            user_agent = self.request.META['HTTP_USER_AGENT']

            # Test common mobile values.
            if self.USER_AGENTS_TEST_SEARCH_REGEX.search(user_agent) and \
                not self.USER_AGENTS_EXCEPTION_SEARCH_REGEX.search(user_agent):
                is_mobile = True
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

                if self.request.META.has_key('HTTP_ACCEPT'):
                    http_accept = self.request.META['HTTP_ACCEPT']
                    if self.HTTP_ACCEPT_REGEX.search(http_accept):
                        is_mobile = True

            if not is_mobile:
                # Now we test the user_agent from a big list.
                if self.USER_AGENTS_TEST_MATCH_REGEX.match(user_agent):
                    is_mobile = True

        return is_mobile
