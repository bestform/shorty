About
-----

shorty is a python library for dealing with url shortening services.
It is in its very early stages, so please feel free to fork it and help.

Currently there are only two resolvers implemented, for is.gd and bit.ly

To use the library with bit.ly, you have to create a (free) account to get an API key.
Just copy the file `settings.py.empty` to `settings.py` and insert your login and key.

You can run the unit tests by either running test.py or by running

    python -m unittest discover

on python 2.7 or later.

Example usage
-------------

    >>> import shorty
    >>> myShorty = shorty.Shorty()
    >>> url = "http://is.gd/T9vnnv"
    >>> resolver = myShorty.getResolverByURL(url)
    >>> resolver.resolve(url)
    'http://tonstube.de'

