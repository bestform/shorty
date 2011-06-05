import urllib2
import settings

class Shorty(object):
    """resolves a given short url if the service is supported"""
    def __init__(self):
        self.resolverMap = {
            "http://is.gd" : ResolverISGD(),
            "http://bit.ly" : ResolverBITLY("http://bit.ly"),
            "http://j.mp" : ResolverBITLY("http://j.mp"),
        }

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
        
