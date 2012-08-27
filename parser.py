import json

from server import *
from virtual_machine import *

def create_server_from(item):
  return Server(id=item['id'], slot_capacity=item['cases'])

def create_vm_from(item):
  return VirtualMachine(id=item['id'], size=item['cases'])

class Parser(object):
  def __extract_json_object_from(self, json_string):
    return json.loads(json_string)

  def __extract_servers_from(self, json_object):
    server_list = json_object['serveurs']
    return [create_server_from(item) for item in server_list]

  def __extract_vms_from(self, json_object):
    vm_list = json_object['machineVirtuelles']
    return [create_vm_from(item) for item in vm_list]

  def from_json(self, json_string):
    json_object = self.__extract_json_object_from(json_string)
    servers = self.__extract_servers_from(json_object)
    vms = self.__extract_vms_from(json_object)
    return (servers, vms)