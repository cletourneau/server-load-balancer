import unittest

from hamcrest import *

from parser import *
from matchers import *

class ParserTestCase(unittest.TestCase):
  def setUp(self):
    self.parser = Parser()

  def test_noJSONServersAndVms_returnsEmptyArrays(self):
    json_string = '{"serveurs":[], "machineVirtuelles":[]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, equal_to([]))
    assert_that(vms, equal_to([]))

  def test_oneServer_returnsIt(self):
    json_string = '{"serveurs":[{"id":"serveur1","cases":4}], "machineVirtuelles":[]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, has_length(1))
    assert_that(servers, contains_a_server_with(id="serveur1", slot_capacity=4))

  def test_multipleServer_returnsThem(self):
    json_string = '{"serveurs":[{"id":"serveur1","cases":4}, {"id":"serveur2","cases":5}, {"id":"serveur3","cases":10}], "machineVirtuelles":[]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, has_length(3))
    assert_that(servers, contains_a_server_with(id="serveur1", slot_capacity=4))
    assert_that(servers, contains_a_server_with(id="serveur2", slot_capacity=5))
    assert_that(servers, contains_a_server_with(id="serveur3", slot_capacity=10))

  def test_oneVm_returnsIt(self):
    json_string = '{"serveurs":[], "machineVirtuelles":[{"id":"VM1","cases":1}]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(vms, has_length(1))
    assert_that(vms, contains_a_vm_with(id="VM1", size=1))

  def test_multipleVm_returnsThem(self):
    json_string = '{"serveurs":[], "machineVirtuelles":[{"id":"VM1","cases":1}, {"id":"VM2","cases":4}, {"id":"VM3","cases":8}]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(vms, has_length(3))
    assert_that(vms, contains_a_vm_with(id="VM1", size=1))
    assert_that(vms, contains_a_vm_with(id="VM2", size=4))
    assert_that(vms, contains_a_vm_with(id="VM3", size=8))

  def test_iweb_json(self):
    json_string = '{"serveurs":[{"id":"serveur1","cases":4},{"id":"serveur2","cases":6}],"machineVirtuelles":[{"id":"VM1","cases":1},{"id":"VM2","cases":4},{"id":"VM3","cases":2}]}'

    (servers, vms) = self.parser.from_json(json_string)

    assert_that(servers, has_length(2))
    assert_that(vms, has_length(3))

    assert_that(servers, contains_a_server_with(id="serveur1", slot_capacity=4))
    assert_that(servers, contains_a_server_with(id="serveur2", slot_capacity=6))

    assert_that(vms, contains_a_vm_with(id="VM1", size=1))
    assert_that(vms, contains_a_vm_with(id="VM2", size=4))
    assert_that(vms, contains_a_vm_with(id="VM3", size=2))

if __name__ == '__main__':
  unittest.main()
