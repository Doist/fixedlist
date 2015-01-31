#!/usr/bin/env python
# Copyright (c) 2007 Qtrac Ltd. All rights reserved.
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from setuptools import setup

setup(name='fixedlist',
      version = '1.0',
      author="amix",
      author_email="amix@amix.dk",
      url="http://www.amix.dk/",
      install_requires = ['redis>=2.7.1'],
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      packages=['fixedlist'],
      include_package_data=True,
      zip_safe=False,
      platforms=["Any"],
      license="BSD",
      keywords='redis fixed list small list short list',
      description="Fast performance fixed list for Redis",
      long_description="""\
fixedlist
---------
This Python library makes it possible to implement a fast fixed list structure for Redis with following properties:

* Fixed size of the list
* Fast inserts, updates and fetches
* Small memory footprint with gziped data
* No duplicates inside the list

Requires Redis 2.6+ and newest version of redis-py.


Installation
------------

Can be installed very easily via::

    $ pip install fixedlist

For more help look at https://github.com/Doist/fixedlist

Copyright: 2015 by Doist Ltd.

Developer: Amir Salihefendic ( http://amix.dk )

License: BSD""")
