import json
import string

from server import *
from virtual_machine import *

ID_KEY = "id"
SLOT_KEY = "cases"
SERVER_KEY = "serveurs"
VM_KEY = "machineVirtuelles"
USAGE_PERCENTAGE_KEY = "pourcentageUtilisation"

def create_server_from(item):
  return Server(id=item[ID_KEY], slot_capacity=item[SLOT_KEY])

def create_vm_from(item):
  return VirtualMachine(id=item[ID_KEY], size=item[SLOT_KEY])

def create_vm_json_for(vm):
  return '{{"{id_key}":"{id}","{slot_key}":{size}}}'.format(
    id_key=ID_KEY,
    id=vm.id,
    slot_key=SLOT_KEY,
    size=vm.size)

def create_server_json_for(server):
  json_vms = [create_vm_json_for(vm) for vm in server.vms]
  return '{{"{id_key}":"{id}","{slot_key}":{slot_capacity},"{usage_percentage_key}":{current_load_percentage},"{vm_key}":[{vms}]}}'.format(
    id_key=ID_KEY,
    id=server.id,
    slot_key=SLOT_KEY,
    slot_capacity=server.slot_capacity,
    usage_percentage_key=USAGE_PERCENTAGE_KEY,
    current_load_percentage=server.current_load_percentage,
    vm_key=VM_KEY,
    vms=string.join(json_vms, ","))

class Parser(object):
  def __extract_json_object_from(self, json_string):
    return json.loads(json_string)

  def __extract_servers_from(self, json_object):
    server_list = json_object[SERVER_KEY]
    return [create_server_from(item) for item in server_list]

  def __extract_vms_from(self, json_object):
    vm_list = json_object[VM_KEY]
    return [create_vm_from(item) for item in vm_list]

  def from_json(self, json_string):
    json_object = self.__extract_json_object_from(json_string)
    servers = self.__extract_servers_from(json_object)
    vms = self.__extract_vms_from(json_object)
    return (servers, vms)

  def to_json(self, servers):
    json_servers = [create_server_json_for(s) for s in servers]

    json = '{{"{server_key}":[{servers}]}}'.format(
      server_key=SERVER_KEY,
      servers=string.join(json_servers, ","))
    return json