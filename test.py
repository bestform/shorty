import unittest
import shorty

class TestURLFuntions(unittest.TestCase):
    
    def setUp(self):
        self.shorty = shorty.Shorty()
        self.resolverPacks = [
            {"name": "http://is.gd", "url": "http://tonstube.de", "shorturl": "http://is.gd/T9vnnv", "handle": "T9vnnv"},
            {"name": "http://bit.ly", "url": "http://tonstube.de/", "shorturl": "http://bit.ly/klSF10", "handle": "klSF10"},
            {"name": "http://j.mp", "url": "http://tonstube.de/", "shorturl": "http://j.mp/klSF10", "handle": "klSF10"},
            {"name": "http://goo.gl", "url": "http://tonstube.de/", "shorturl": "http://goo.gl/ezv5G", "handle": "ezv5G"},
        ]
        self.shortenerPacks = [
            {"name": "http://is.gd", "url": "http://tonstube.de"},
            {"name": "http://bit.ly", "url": "http://tonstube.de/"},
            {"name": "http://j.mp", "url": "http://tonstube.de/"},
            {"name": "http://goo.gl", "url": "http://tonstube.de/"}
        ]

    def testUnknowResolver(self):
        self.assertRaises(ValueError, self.shorty.getResolverByName, "unknown")

    def testResolvers(self):
        for res in self.resolverPacks:
            resolver = self.shorty.getResolverByURL(res["shorturl"])
            self.assertEqual(resolver.name, res["name"])
            self.assertRaises(AttributeError, resolver.resolve, "unknown")
            self.assertRaises(AttributeError, resolver.resolve, res["name"])
            self.assertEqual(resolver.getHandle(res["shorturl"]), res["handle"])
            self.assertEqual(resolver.resolve(res["shorturl"]), res["url"])

    def testShorteners(self):
        for sho in self.shortenerPacks:
            shortener = self.shorty.getShortenerByName(sho["name"])
            self.assertEqual(shortener.name, sho["name"])
            shortURL = shortener.shorten(sho["url"])
            resolver = self.shorty.getResolverByURL(shortURL)
            longURL = resolver.resolve(shortURL)
            self.assertEqual(sho["url"], longURL)
            self.assertTrue(shortURL.startswith(sho["name"]))

if __name__ == "__main__":
    unittest.main()
