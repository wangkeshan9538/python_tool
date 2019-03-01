# -*- coding: utf-8
import redis
import threading

locks = threading.local()


def key_for(user_id):
    return "account_{}".format(user_id)

def _lock(client, key):
    return bool(client.set(key, "True", nx=True, ex=5))

def _unlock(client, key):
    client.delete(key)


def lock(client, user_id):
    key = key_for(user_id)
    if key in locks.redis:
        locks.redis[key] += 1
        return True
    ok = _lock(client, key)
    if not ok:
        return False
    locks.redis[key] = 1
    return True


def unlock(client, user_id):
    key = key_for(user_id)
    if key in locks.redis:
        locks.redis[key] -= 1
        if locks.redis[key] <= 0:
            del locks.redis[key]
            unlock(client,user_id)
        return True
    return False


def run():
    locks.redis = {}
    print (threading.current_thread().name, "lock", lock(client, "codehole"))
    print (threading.current_thread().name, "lock", lock(client, "codehole"))
    print (threading.current_thread().name, "unlock", unlock(client, "codehole"))
    print (threading.current_thread().name, "unlock", unlock(client, "codehole"))



if __name__=='__main__':
    client = redis.StrictRedis()
    t = threading.Thread(target=run, name='Thread1')
    t2 = threading.Thread(target=run, name='Thread2')
    t.start()
    t2.start()