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

try:
    import cPickle as pickle
except ImportError:
    import pickle

class RedisDBA(object):

    def __init__(self, rdb_uri):

        log.msg('connect: %s'%redis_uri)
        self.rdb = redis.StrictRedis.from_url(rdb_uri)

    def filter(self, item):

        return True

class MongoDBA(object):

    def __init__(self, mongo_uri):

        log.msg('connect: %s'%mongo_uri)
        parsed = pymongo.uri_parser.parse_uri(mongo_uri)
        host, port = parsed['nodelist'][0]
        db, tbl = parsed['database'], parsed['collection']
        self.mdb = pymongo.MongoClient(host, port)[db][tbl]

    def get_pk(self, item):

        if '_pk' in item:
            pk = item['_pk']
            del item['_pk']
            return pk

        for pk in ['oid', 'mid']:
            if pk in item:
                return pk

    def save(self, item):

        try:
            pk = self.get_pk(item)
            if pk:
                pv = item[pk]
                self.mdb.update({pk:pv}, item, upsert=True)
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

    def process(self, msg):

        try:
            buf = msg[0]
            item = pickle.loads(buf)
            if self.rdba.filter(item):
                self.mdba.save(item)
        except:
            log.err()

    def run(self):

        reactor.run()

if __name__=='__main__':

    #log.startLogging(DailyLogFile.fromFullPath("/tmp/alibaba-broker.log"))
    log.startLogging(sys.stdout)

    Broker('tcp://*:1688').run()

