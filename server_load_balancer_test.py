from hamcrest import *
import unittest
from server_load_balancer import *
from server import *
from virtual_machine import *
from matchers import *

class ServerLoadBalancerTestCase(unittest.TestCase):
  def setUp(self):
    self.server_balancer = ServerLoadBalancer()

  def test_oneServerNoVms_serverStaysEmpty(self):
    server = Server(id="server_id", slot_capacity=1)
    empty_vms = []

    self.server_balancer.balance([server], empty_vms)

    assert_that(server, has_current_load_percentage_of(0))

  def test_serverOneSlotCapacity_withOneSlotVm_serverIsFullyLoaded(self):
    server = Server(id="server_id", slot_capacity=1)
    vm = VirtualMachine(id="vm_id", size=1)

    self.server_balancer.balance([server], [vm])

    assert_that(server, has_current_load_percentage_of(100))
    assert_that(server, has_a_vm_count_of(1))
    assert_that(vm, is_loaded_in(server))

  def test_serverThreeSlotsCapacity_withTwoSlotVm_serverIs67PercentLoaded(self):
    server = Server(id="server_id", slot_capacity=3)
    vm = VirtualMachine(id="vm_id", size=2)

    self.server_balancer.balance([server], [vm])

    assert_that(server, has_current_load_percentage_of(67))
    assert_that(server, has_a_vm_count_of(1))
    assert_that(vm, is_loaded_in(server))

  def test_serverTenSlotsCapacity_withOneSlotVm_serverIsTenPercentLoaded(self):
    server = Server(id="server_id", slot_capacity=10)
    vm = VirtualMachine(id="vm_id", size=1)

    self.server_balancer.balance([server], [vm])

    assert_that(server, has_current_load_percentage_of(10))
    assert_that(server, has_a_vm_count_of(1))
    assert_that(vm, is_loaded_in(server))

  def test_serverTenSlotsCapacity_withTwoOneSlotVms_serverIsTwentyPercentLoaded(self):
    server = Server(id="server_id", slot_capacity=10)
    vm1 = VirtualMachine(id="vm1", size=1)
    vm2 = VirtualMachine(id="vm2", size=1)

    self.server_balancer.balance([server], [vm1, vm2])

    assert_that(server, has_current_load_percentage_of(20))
    assert_that(server, has_a_vm_count_of(2))
    assert_that(vm1, is_loaded_in(server))
    assert_that(vm2, is_loaded_in(server))

if __name__ == '__main__':
  unittest.main()
