import unittest

from hamcrest import *

from server_load_balancer import *
from matchers.current_load_percentage_of_server import *
from matchers.vm_count_of_server import *
from matchers.vm_is_loaded_in_server import *

class ServerLoadBalancerTestCase(unittest.TestCase):
  def setUp(self):
    self.server_balancer = ServerLoadBalancer()

  def test_oneServerNoVms_serverStaysEmpty(self):
    server = Server(id="server1", slot_capacity=1)
    empty_vms = []

    self.server_balancer.balance([server], empty_vms)

    assert_that(server, has_current_load_percentage_of(0))

  def test_serverOneSlotCapacity_withOneSlotVm_serverIsFullyLoaded(self):
    server = Server(id="server1", slot_capacity=1)
    vm = VirtualMachine(id="vm1", size=1)

    self.server_balancer.balance([server], [vm])

    assert_that(server, has_current_load_percentage_of(100))
    assert_that(server, has_a_vm_count_of(1))
    assert_that(vm, is_loaded_in(server))

  def test_serverTenSlotsCapacity_withOneSlotVm_serverIsTenPercentLoaded(self):
    server = Server(id="server1", slot_capacity=10)
    vm = VirtualMachine(id="vm1", size=1)

    self.server_balancer.balance([server], [vm])

    assert_that(server, has_current_load_percentage_of(10))
    assert_that(server, has_a_vm_count_of(1))
    assert_that(vm, is_loaded_in(server))

  def test_serverTenSlotsCapacity_withTwoOneSlotVms_serverIsTwentyPercentLoaded(self):
    server = Server(id="server1", slot_capacity=10)
    vm1 = VirtualMachine(id="vm1", size=1)
    vm2 = VirtualMachine(id="vm2", size=1)

    self.server_balancer.balance([server], [vm1, vm2])

    assert_that(server, has_current_load_percentage_of(20))
    assert_that(server, has_a_vm_count_of(2))
    assert_that(vm1, is_loaded_in(server))
    assert_that(vm2, is_loaded_in(server))

  def test_vmShouldLoadOnLessLoadedServerFirst(self):
    server1 = Server(id="server1", slot_capacity=100)
    server1.add_vm(VirtualMachine(id="server1_vm", size=1))

    server2 = Server(id="server2", slot_capacity=1)
    vm = VirtualMachine(id="vm", size=1)

    self.server_balancer.balance([server1, server2], [vm])

    assert_that(vm, is_loaded_in(server2))

  def test_serverWithNotEnoughCapacity_shouldNotBeLoaded_withAVm(self):
    server = Server(id="server1", slot_capacity=4)
    vm = VirtualMachine(id="vm1", size=5)

    self.server_balancer.balance([server], [vm])

    assert_that(vm, is_not(is_loaded_in(server)))

  def test_iweb_expectations(self):
    server1 = Server(id="server1", slot_capacity=4)
    server2 = Server(id="server2", slot_capacity=6)
    vm1 = VirtualMachine(id="vm1", size=1)
    vm2 = VirtualMachine(id="vm2", size=4)
    vm3 = VirtualMachine(id="vm3", size=2)

    self.server_balancer.balance([server1, server2], [vm1, vm2, vm3])

    assert_that(vm1, is_loaded_in(server1))
    assert_that(vm2, is_loaded_in(server2))
    assert_that(vm3, is_loaded_in(server1))

    assert_that(server1, has_current_load_percentage_of(75))
    assert_that(server2, has_current_load_percentage_of(67))

if __name__ == '__main__':
  unittest.main()
