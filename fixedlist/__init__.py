import types
import zlib
import redis

from redis import WatchError

DEFAULT_RETRIES = 5


#--- System specific ----------------------------------------------
REDIS_SYSTEMS = {}

def set_redis(system_name='default', redis_host='localhost',
              redis_port=6379, db=0, **kw):
    """Setup a system."""
    REDIS_SYSTEMS[system_name] = redis.Redis(host=redis_host,
                                        port=redis_port,
                                        db=db, **kw)

def get_redis(system='default'):
    return REDIS_SYSTEMS.get(system)


#--- List functions ----------------------------------------------
def get(list_key, system='default'):
    """Return list with key `list_key`.

    If a list isn't created, then an empty list is returned.
    """
    result = get_redis(system).get(list_key)
    return _decode_list_row(result)


def get_multi(list_keys, system='default'):
    """Return a dictionary of lists with keys `list_keys`.

    If a list isn't created, then an entry with an empty list is returned.
    """
    result = {}

    results = get_redis(system).mget(list_keys)

    for i, key in enumerate(list_keys):
        result[key] = _decode_list_row(results[i])

    return result



def _multi_list_op(list_keys, values_to_add, modify, check=None, system='default', limit=200, retries=DEFAULT_RETRIES):
    if not check:
        check = lambda k, l, vta: True

    list_keys = _ensure_list(list_keys)
    values_to_add = _ensure_list(values_to_add)

    r = get_redis(system)
    with r.pipeline() as p:
        while retries > 0:
            try:
                for k in list_keys:
                    p.watch(k)
                current_values = {}
                for k in list_keys:
                    current_values[k] = _decode_list_row(p.get(k))

                should_update = False
                for key, current_list in current_values.iteritems():
                    if check(key, current_list, values_to_add):
                        should_update = True
                        break

                if not should_update:
                    p.unwatch()
                    return

                p.multi()
                for key, current_list in current_values.iteritems():
                    new_list = modify(key, list(current_list), values_to_add, limit)
                    if current_list != new_list:
                        p.set(key, _encode_list(new_list))
                p.execute()
                return current_values
            except WatchError:
                retries -= 1
                continue

def add(list_keys, values_to_add, system='default', limit=200, retries=DEFAULT_RETRIES):
    """Add `values_to_add` to lists with keys `list_keys`.

    Example::

        >>> fixed_list.add(['key1', 'key3'], ['some value'])
        >>> fixed_list.add('key1', ['some value'])
    """
    def check(k, l, vta):
        x = any(val not in l for val in vta)
        return x

    def modify(k, l, vta, limit):
        only_new = [ val for val in vta if val not in l ]
        if len(only_new) > 0:
            l.extend(only_new)
        return l[-limit:]
    _multi_list_op(list_keys, values_to_add, modify, check, system, limit, retries)


def remove(list_keys, values_to_remove, system='default', retries=DEFAULT_RETRIES):
    """Remove `values_to_remove` from lists with keys `list_keys`.

    Example::

        >>> fixed_list.add(['key1', 'key3'], ['some value'])
        >>> fixed_list.add('key1', ['some value'])
    """

    def check(k, l, vtr):
        return any(val in l for val in vtr )

    def modify(k, l, vtr, limit):
        start_len = len(l)
        for v in vtr:
            try:
                l.remove(v)
            except:
                pass
        if start_len > len(l):
            return l

    return _multi_list_op(list_keys, values_to_remove, modify, check, system, None, retries)

def set(list_keys, values, system='default'):
    """Set lists with keys `list_keys` to `values`.

    Example::

        >>> fixed_list.set(['key1', 'key3'], ['1', '2'])
        >>> fixed_list.set('key1', ['1', '2'])
    """
    list_keys = _ensure_list(list_keys)
    values = _ensure_list(values)
    values = _encode_list(values)

    if not list_keys:
        return

    r = get_redis(system)
    with r.pipeline() as p:
        p.multi()
        for key in list_keys:
            p.set(key, values)
        p.execute()

    return True


def empty(list_keys, system='default'):
    """Reset lists with keys `list_keys`.

    Example::

        >>> fixed_list.list_empty(['test'])
    """
    set(list_keys, [], system)
    return True


def varnish(list_keys, system='default'):
    """Delete lists completely with keys `list_keys`."""
    list_keys = _ensure_list(list_keys)

    if not list_keys:
        return

    r = get_redis(system)
    with r.pipeline() as p:
        p.multi()
        for key in list_keys:
            p.delete(key)
        p.execute()
    return True


#--- Internal ----------------------------------------------
def _decode_list_row(value):
    if not value:
        return []
    value = zlib.decompress(value)
    return [ v for v in value.split(r'~') if v ]

def _encode_list(list_value):
    if not list_value:
        return ''

    v_encoded = []
    for v in list_value:
        v_encoded.append('%s~' % v)
    result = ''.join(v_encoded)
    return zlib.compress(result)

def _ensure_list(some_value):
    if type(some_value) == types.ListType:
        return some_value
    else:
        return [some_value]
