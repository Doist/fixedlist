fixedlist: fast performance fixed list for Redis
================================================

This Python library makes it possible to implement a fast fixed list structure for Redis with following properties:

* Fast inserts, updates and fetches
* 2x faster perfomance than pure Redis implementation
* 1.4x less memory footpring (due to gziped data)
* No duplicates inside the list

Requires Redis 2.6+ and newest version of redis-py.


Installation
============

Can be installed very easily via

    $ pip install fixedlist


Benchmark
=========

Testing fixedlist against a pure Redis implementaiton of a fixedlist yields good results.

The benchmarks are in the `benchmark/` folder and they store 300 lists with 200 values each. The lists are int and strings lists.

* fixedlist is about 2.4x faster (47s vs. 117s on a Mac Book Pro from 2014)
* fixedlist uses 1.4x less memory (1.24MB vs. 1.84MB)

The benchmark is run in a following way:

* time python benchmark/benchmark_fixed_list.py
* time python benchmark/benchmark_python_redis.py

Redis stats are fetched from `redis-cli info` command.


Examples
========

Setting things up:

```python
import fixedlist
fixedlist.set_redis(redis_host='locahost', redis_port=6380)
```

Add a value to a list:

```python
fixedlist.add('hello', 'world')
assert fixedlist.get('hello') == ['world']
```

Add mutliple values to multiple keys at once:

```python
fixedlist.add(['hello1', 'hello2'], ['world1', 'world2'])
assert fixedlist.get('hello1') == ['world1', 'world2']
```

Fetch multiple at once:

```python
assert fixedlist.get_multi(['hello1', 'hello2']) ==\
       {'hello1': ['world1', 'world2'],
        'hello2': ['world1', 'world2']}
```

Remove a value:

```python
fixedlist.remove('hello', 'world1')
assert fixedlist.get('hello') == ['world2']
```

Handle duplicates

```python
fixedlist.empty('hello')
fixedlist.add('hello', 'world')
fixedlist.add('hello', 'world')
assert fixedlist.get('hello') == ['world']
```


Full API
========

Redis related:

* `fixedlist.set_redis(system_name='default', redis_host='localhost', redis_port=6379, **redis_kws)`: Setup Redis
* `fixedlist.get_redis(system='default')`: Return a Redis client to `system`

List fetches:

* `fixedlist.get(list_key, system='default')`: Return values for `list_key`
* `fixedlist.get_multi(list_keys, system='default')`: Return a dictionary of values for `list_keys`

List adding/setting:

* `fixedlist.add(list_keys, values_to_add, system='default', limit=200)`: Add `values_to_add` to `list_keys`. Limit the size of `list_keys` to `limit`
* `fixedlist.set(list_keys, values, system='default')`: Set `list_keys` to `values`

List removing/resetting:

* `fixedlist.remove(list_keys, values_to_remove, system='default')`: Remove `values_to_remove` from `list_keys`
* `fixedlist.empty(list_keys, system='default')`: Empty the values of `list_keys`
* `fixedlist.varnish(list_keys, system='default')`: Delete `list_keys` keys


Copyright
=========

2018 by Doist Ltd.


Developer
=========

[Amir Salihefendic](http://amix.dk)


License
=======

MIT
