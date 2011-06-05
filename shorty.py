import urllib2
import urllib
import settings

class Shorty(object):
    """resolves a given short url if the service is supported"""
    def __init__(self):
        self.resolverMap = {
            "http://is.gd" : ResolverISGD(),
            "http://bit.ly" : ResolverBITLY("http://bit.ly"),
            "http://j.mp" : ResolverBITLY("http://j.mp"),
        }
        self.shortenerMap = {
            "http://is.gd" : ShortenerISGD(),
            "http://bit.ly" : ShortenerBITLY("http://bit.ly"),
            "http://j.mp" : ShortenerBITLY("http://j.mp")
        }

    def getShortenerByName(self, name):
        try:
            shortener = self.shortenerMap[name]
        except KeyError:
            raise ValueError("unknown resolver: " + name)
        return shortener

    def getResolverByName(self, name):
        try:
            resolver = self.resolverMap[name]
        except KeyError:
            raise ValueError("unknown resolver: " + name)
        return resolver

    def getResolverByURL(self, url):
        if not url.startswith("http://"):
            raise AttributeError("wrong URL")
        name = url[0:url.find("/", 7)]
        return self.getResolverByName(name)


"""
Shortener
"""

class Shortener(object):
    """A service to shorten urls"""
    def __init__(self):
        raise NotImplementedError("Abstract Shortener cannot be initialized.")

    def shorten(self, url):
        encodedURL = urllib.quote_plus(url)
        ret = urllib2.urlopen(self.api+encodedURL)
        return ret.read().rstrip('\n')

class ShortenerISGD(Shortener):
    """A shortener for is.gd"""
    def __init__(self):
        self.name = "http://is.gd"
        self.api = "http://is.gd/create.php?format=simple&url="

class ShortenerBITLY(Shortener):
    """A shortener for bit.ly"""
    def __init__(self, name):
        self.name = name
        self.api = "http://api.bitly.com/v3/shorten?login="+settings.bitly_login+"&apiKey="+settings.bitly_api_key+"&format=txt&longUrl="

"""
Resolver
"""

class Resolver(object):
    """A service to resolve urls"""
    def __init__(self):
        raise NotImplementedError("Abstract Resolver cannot be initialized.")

    def testURL(self, url):
        if not url.startswith(self.name):
            raise AttributeError("Not a correct URL")
        idx = url.rfind("/")
        if not idx > 6:
            raise AttributeError("Can't parse URL")

    def getHandle(self, url):
        idx = url.rfind("/")
        return url[idx+1:]

    def resolve(self, url):
        self.testURL(url)
        handle = self.getHandle(url)
        ret = urllib2.urlopen(self.api + handle)
        return ret.read().rstrip('\n')

class ResolverISGD(Resolver):
    """A resolver for is.gd"""
    def __init__(self):
        self.name = "http://is.gd"
        self.api = "http://is.gd/forward.php?format=simple&shorturl="


class ResolverBITLY(Resolver):
    """A resolver for bit.ly"""
    def __init__(self, name):
        self.name = name
        self.api = "http://api.bitly.com/v3/expand?apiKey="+settings.bitly_api_key+"&login="+settings.bitly_login+"&format=txt&hash="
        
