import unittest

from hamcrest import *

from parser import *
from matchers.server_list_contains import *
from matchers.vm_list_contains import *

class ParserTestCase(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_from_json_noServersAndVms_returnsEmptyArrays(self):
    json_string = '{"serveurs":[], "machineVirtuelles":[]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, equal_to([]))
    assert_that(vms, equal_to([]))

  def test_from_json_oneServer_returnsIt(self):
    json_string = '{"serveurs":[{"id":"serveur1","cases":4}], "machineVirtuelles":[]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, has_length(1))
    assert_that(servers, contains_a_server_with(id="serveur1", slot_capacity=4))

  def test_from_json_multipleServer_returnsThem(self):
    json_string = '{"serveurs":[{"id":"serveur1","cases":4}, {"id":"serveur2","cases":5}, {"id":"serveur3","cases":10}], "machineVirtuelles":[]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, has_length(3))
    assert_that(servers, contains_a_server_with(id="serveur1", slot_capacity=4))
    assert_that(servers, contains_a_server_with(id="serveur2", slot_capacity=5))
    assert_that(servers, contains_a_server_with(id="serveur3", slot_capacity=10))

  def test_from_json_oneVm_returnsIt(self):
    json_string = '{"serveurs":[], "machineVirtuelles":[{"id":"VM1","cases":1}]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(vms, has_length(1))
    assert_that(vms, contains_a_vm_with(id="VM1", size=1))

  def test_from_json_multipleVm_returnsThem(self):
    json_string = '{"serveurs":[], "machineVirtuelles":[{"id":"VM1","cases":1}, {"id":"VM2","cases":4}, {"id":"VM3","cases":8}]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(vms, has_length(3))
    assert_that(vms, contains_a_vm_with(id="VM1", size=1))
    assert_that(vms, contains_a_vm_with(id="VM2", size=4))
    assert_that(vms, contains_a_vm_with(id="VM3", size=8))

  def test_from_json_iweb(self):
    json_string = '{"serveurs":[{"id":"serveur1","cases":4},{"id":"serveur2","cases":6}],"machineVirtuelles":[{"id":"VM1","cases":1},{"id":"VM2","cases":4},{"id":"VM3","cases":2}]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, has_length(2))
    assert_that(vms, has_length(3))

    assert_that(servers, contains_a_server_with(id="serveur1", slot_capacity=4))
    assert_that(servers, contains_a_server_with(id="serveur2", slot_capacity=6))

    assert_that(vms, contains_a_vm_with(id="VM1", size=1))
    assert_that(vms, contains_a_vm_with(id="VM2", size=4))
    assert_that(vms, contains_a_vm_with(id="VM3", size=2))

  #

  def test_to_json_noServer(self):
    actual_json = self.parser.to_json([])

    assert_that(actual_json, equal_to('{"serveurs":[]}'))

  def test_to_json_oneEmptyServer(self):
    server = Server(id="server1", slot_capacity=8)
    actual_json = self.parser.to_json([server])

    assert_that(actual_json, equal_to('{"serveurs":[{"id":"server1","cases":8,"pourcentageUtilisation":0,"machineVirtuelles":[]}]}'))

  def test_to_json_twoEmptyServers(self):
    server1 = Server(id="server1", slot_capacity=8)
    server2 = Server(id="server2", slot_capacity=4)
    actual_json = self.parser.to_json([server1, server2])

    assert_that(actual_json, equal_to('{"serveurs":[{"id":"server1","cases":8,"pourcentageUtilisation":0,"machineVirtuelles":[]},{"id":"server2","cases":4,"pourcentageUtilisation":0,"machineVirtuelles":[]}]}'))

  def test_to_json_oneServer_withOneVm(self):
    server = Server(id="server1", slot_capacity=8)
    server.add_vm(VirtualMachine(id="vm1", size=3))
    actual_json = self.parser.to_json([server])

    assert_that(actual_json, equal_to('{"serveurs":[{"id":"server1","cases":8,"pourcentageUtilisation":38,"machineVirtuelles":[{"id":"vm1","cases":3}]}]}'))

  def test_to_json_iweb(self):
    server1 = Server(id="serveur1", slot_capacity=4)
    server1.add_vm(VirtualMachine(id="VM1", size=1))
    server1.add_vm(VirtualMachine(id="VM3", size=2))

    server2 = Server(id="serveur2", slot_capacity=6)
    server2.add_vm(VirtualMachine(id="VM2", size=4))

    actual_json = self.parser.to_json([server1, server2])
    assert_that(actual_json, equal_to('{"serveurs":[{"id":"serveur1","cases":4,"pourcentageUtilisation":75,"machineVirtuelles":[{"id":"VM1","cases":1},{"id":"VM3","cases":2}]},{"id":"serveur2","cases":6,"pourcentageUtilisation":67,"machineVirtuelles":[{"id":"VM2","cases":4}]}]}'))

if __name__ == '__main__':
  unittest.main()
