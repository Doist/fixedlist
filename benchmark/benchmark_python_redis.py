import random
import string

import fixedlist

KEYS = 300
VALUES = 250

def main():
    fixedlist.set_redis(redis_host='0.0.0.0', redis_port=6380)
    rcli = fixedlist.get_redis()

    # Ints
    for i in xrange(0, KEYS):
        list_key = 'test_list_i_%s' % i
        rcli.delete(list_key)
        for i in range(0, VALUES):
            list_add(rcli, list_key, [i, i+1])
            assert len(list_get(rcli, list_key)) <= 200

    # Strings
    for i in xrange(0, KEYS):
        list_key = 'test_list_s_%s' % i
        rcli.delete(list_key)
        for i in range(0, VALUES):
            list_add(rcli, list_key, [randomword(6), randomword(6)])
            assert len(list_get(rcli, list_key)) <= 200

def list_add(rcli, list_key, values, limit=200):
    with rcli.pipeline() as p:
        p.watch(list_key)
        for value in values:
            p.lrem(list_key, value)
            p.lpush(list_key, value)
        p.ltrim(list_key, 0, limit-1)
        p.unwatch()

def list_get(rcli, list_key, limit=200):
    return rcli.lrange(list_key, 0, limit)

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

if __name__ == '__main__':
    main()
