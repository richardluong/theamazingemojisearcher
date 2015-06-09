class Emoji(object):
    """docstring for Emoji"""
    def __init__(self,
                 index="",
                 code="",
                 browser="",
                 bw="",
                 apple="",
                 andr="",
                 twit="",
                 gmail="",
                 wind="",
                 name="",
                 version="",
                 default="",
                 annotations="",
                 emojipedia_url="",
                 uni="",
                 desc="",
                 related_to=[],
                 known_as=[]):
        self.index = index
        self.code = code
        self.browser = browser
        self.bw = bw
        self.apple = apple
        self.andr = andr
        self.twit = twit
        self.gmail = gmail
        self.wind = wind
        self.name = name
        self.version = version
        self.default = default
        self.annotations = annotations
        self.emojipedia_url = emojipedia_url
        self.uni = uni
        self.desc = desc
        self.related_to = related_to
        self.known_as = known_as

    def print_emoji(self):
        """Prints emoji"""
        print "index:", self.index
        print "name:", self.name
        print "browser:", self.browser
        print "desc:", self.desc
        print "known_as:", self.known_as
        print "related_to:", self.related_to
        print "annotations", self.annotations
        print "ep url:", self.emojipedia_url

