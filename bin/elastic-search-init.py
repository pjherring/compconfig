#! /usr/bin/env python

import logging
import argparse
import json
import urllib2

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

ENV_MAP = {
  'dev' : {
    'elastic-host' : 'localhost',
    'rabbit-host' : 'localhost'
  },
  'stag' : {
    'elastic-host' : 'nyc-selasticsearch-1.sta.peer1.squarespace.net',
    'rabbit-host' : 'nyc-srmq01.sta.peer1.squarespace.net',
  }
}

RABBIT_PORT = 5672
ELASTIC_PORT = 9200
INDEX_NAME = 'sqsp'

CREATE_INDEX_DATA = {
  'mappings' : {
    'ContentCollection': {
      '_routing' : {
        'path' : 'websiteId',
        'required' : True
      }
    },
    'PageCollectionData': {
      '_routing' : {
        'path' : 'websiteId',
        'required' : True
      }
    },
    'ContentItem': {
      '_routing' : {
        'path' : 'websiteId',
        'required' : True
      },
      '_parent' : {
        'type' : 'ContentCollection'
      }
    },
  }
}

init_rabbit_data = {
  "type" : "rabbitmq",
  "rabbitmq" : {
    "host" : "localhost",
    "port" : RABBIT_PORT,
    "user" : "guest",
    "pass" : "guest",
    "vhost" : "/",
    "queue" : "ELASTIC_SEARCH",
    "exchange" : "Squarespace",
    "exchange_declare" : True,
    "exchange_type" : "direct",
    "exchange_durable" : True,
    "queue_declare" : True,
    "queue_bind" : True,
    "queue_durable" : True,
    "queue_auto_delete" : False,
    "heartbeat" : "30m"
  },
  "index" : {
    "bulk_size" : 1,
    "bulk_timeout" : "10ms",
    "ordered" : False,
    "number_of_shards" : 5
  }
}

class RequestWithMethod(urllib2.Request):
  def __init__(self, method, *args, **kwargs):
    self._method = method
    urllib2.Request.__init__(self, *args, **kwargs)

  def get_method(self):
    return self._method

def main():
  parser = create_argparser()
  args = parser.parse_args()
  env_vars = ENV_MAP[args.env]

  if (args.op == 'create_index'):
    create_index_operation(env_vars)
  elif (args.op == 'init_rabbit'):
    init_rabbit(env_vars)

def init_rabbit(opts):
  url = "http://%s:%d/_river/rabbitmq_river/_meta" % (opts['elastic-host'], ELASTIC_PORT)
  init_rabbit_data['rabbitmq']['host'] = opts['rabbit-host']

  logging.info("url %s", url)
  logging.info("data %s", init_rabbit_data)

  request = RequestWithMethod('PUT', url, json.dumps(init_rabbit_data))
  response = None

  try:
    response = urllib2.urlopen(request)
  except urllib2.URLError as e:
    if hasattr(e, 'read'):
      logging.error("Error installing rabbitmq river plugin: %s", e.read())
    else:
      logging.error("Error installing rabbitmq river plugin: %s", e)

  if response:
    logging.info("Response: %s", json.loads(response.read()))
  


def create_index_operation(opts):

  create_url = "http://%s:%d/%s" % (opts['elastic-host'], ELASTIC_PORT, INDEX_NAME)
  request = RequestWithMethod('PUT', create_url, json.dumps(CREATE_INDEX_DATA))

  try:
    response = urllib2.urlopen(request)
  except urllib2.URLError as e:
    logging.error("Error creating index %s", e.read())

def create_argparser():
  parser = argparse.ArgumentParser(description='Elastic Search manager')
  parser.add_argument('op', help='Operation to perform', choices=['create_index', 'init_rabbit', 'start'])
  parser.add_argument('-e', dest='env', help="Environment", choices=['prod', 'stag', 'dev'], default='dev')
  return parser

if __name__ == "__main__":
  main()
