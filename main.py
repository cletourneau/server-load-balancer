#!/usr/bin/python

import sys

from parser import *
from server_load_balancer import *

def extract_json_from_file(filename):
  json_file = sys.argv[1]
  f = open(json_file, 'ro')
  return f.read()


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print "Missing JSON input file"
    sys.exit(-1)

  json_input = extract_json_from_file(sys.argv[1])

  print 'Parsing JSON entry'
  parser = Parser()
  (servers, vms) = parser.from_json(json_input)
  print 'Balancing %d virtual machines on %d servers' % (len(vms), len(servers))

  balancer = ServerLoadBalancer()
  balancer.balance(servers, vms)

  print "*** Result ***"
  print parser.to_json(servers)
