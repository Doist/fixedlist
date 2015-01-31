import random
import string

import fixedlist

KEYS = 300
VALUES = 250

def main():
    fixedlist.set_redis(redis_host='0.0.0.0', redis_port=6380)

    # Ints
    for i in xrange(0, KEYS):
        list_key = 'test_list_%s' % i
        fixedlist.varnish(list_key)
        for i in range(0, VALUES):
            fixedlist.add(list_key, [i, i+1])
            assert len(fixedlist.get(list_key)) <= 200

    # Strings
    for i in xrange(0, KEYS):
        list_key = 'test_list_%s' % i
        fixedlist.varnish(list_key)
        for i in range(0, VALUES):
            fixedlist.add(list_key, [randomword(6), randomword(6)])
            assert len(fixedlist.get(list_key)) <= 200

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

if __name__ == '__main__':
    main()
