#!/usr/bin/env python
# simple broker for webbot

from twisted.internet import reactor
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPullConnection
import logging
import math
import pymongo
import redis
import sys
import time

try:
    import cPickle as pickle
except ImportError:
    import pickle

#########################################
# -------------- timeline ------------- #
# all -> pending -> running -> finished #
#########################################

class ItemParser(object):

    metas = {
        'alibaba:go:idx': {
            'mp': 'alibaba:go', # mongo prefix
            'mk': 'oid',        # mongo key
            'rp': 'alibaba:go', # redis prefix
            'rk': 'pending',    # redis key
            'rv': 'oid',        # redis val
        },
        'alibaba:go:detail': {
            'mp': 'alibaba:go', # mongo prefix
            'mk': 'oid',        # mongo key
            'rp': 'alibaba:go', # redis prefix
            'rk': 'finished',   # redis key
            'rv': 'oid',        # redis val
        }
    }

    def parse(self, data):

        meta = self.metas[data['_meta']]
        del data['_meta']
        return data, meta

class RedisDBA(object):

    def __init__(self, rdb_uri):

        log.msg('connect: %s'%rdb_uri)
        self.rdb = redis.StrictRedis.from_url(rdb_uri)

    def filter(self, item, meta):

        rp = meta['rp']
        rk = meta['rk']
        rv = meta['rv']

        val = item[rv]

        if rk=='pending':

            skey = '{}:all'.format(rp)
            sval = val

            if self.rdb.sadd(skey, sval):

                # timeline
                zkey = '{}:timeline'.format(rp)
                zval = val
                zscore = int(time.time())
                self.rdb.zadd(zkey, zscore, zval)

                # pending
                lkey = '{}:pending'.format(rp)
                lval = val
                self.rdb.rpush(lkey, lval)

                return True

            else:

                # finished
                zkey = '{}:finished'.format(rp)
                zval = val
                if self.rdb.zrank(zkey, zval)!=None:
                    return False

                # timeline
                zkey = '{}:timeline'.format(rp)
                zval = val
                zscore = self.rdb.zscore(zkey, zval)
                now = int(time.time())
                delta = now-zscore

                if delta>3600:

                    # timeline
                    zscore = now
                    self.rdb.zadd(zkey, zscore, zval)

                    # pending
                    lkey = '{}:pending'.format(rp)
                    lval = val
                    self.rdb.lpush(lkey, lval)
                    return True

                else:

                    return False

        elif rk=='finished':

            # finished
            zkey = '{}:finished'.format(rp)
            zval = val
            zscore = int(time.time())
            return self.rdb.zadd(zkey, zscore, zval)

        else:

            return True

class MongoDBA(object):

    def __init__(self, mongo_uri):

        log.msg('connect: %s'%mongo_uri)
        parsed = pymongo.uri_parser.parse_uri(mongo_uri)
        host, port = parsed['nodelist'][0]
        db, tbl = parsed['database'], parsed['collection']
        self.mdb = pymongo.MongoClient(host, port)[db][tbl]

    def save(self, item, meta):

        try:
            mk = meta.get('mk')
            if mk:
                self.mdb.update({mk:item[mk]}, item, upsert=True)
            else:
                self.mdb.insert(item)
        except:
            pass

class Broker(object):

    def __init__(self, zmq_uri, rdb_uri, mdb_uri):

        log.msg('bind: %s'%zmq_uri)

        ze = ZmqEndpoint('bind', zmq_uri)
        zf = ZmqFactory()
        zf.registerForShutdown()
        self.cnn = ZmqPullConnection(zf, ze)
        self.cnn.onPull = self.process
        self.rdba = RedisDBA(rdb_uri)
        self.mdba = MongoDBA(mdb_uri)
        self.parse = ItemParser().parse

    def process(self, msg):

        try:
            buf = msg[0]
            data = pickle.loads(buf)
            item, meta = self.parse(data)
            if self.rdba.filter(item, meta):
                self.mdba.save(item, meta)
        except:
            log.err()

    def run(self):

        reactor.run()

if __name__=='__main__':

    #log.startLogging(DailyLogFile.fromFullPath("/tmp/alibaba-broker.log"))
    log.startLogging(sys.stdout)

    zmq_uri = 'tcp://*:1688'
    rdb_uri = 'redis://localhost:6379/9'
    mdb_uri = 'mongodb://localhost:27017/alibaba.go'
    Broker(zmq_uri, rdb_uri, mdb_uri).run()
