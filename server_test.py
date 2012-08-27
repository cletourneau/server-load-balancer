import unittest

from hamcrest import *

from server import *
from virtual_machine import *

class ServerTestCase(unittest.TestCase):
  def test_aServer_canFit_VmsSmallerOrEqualOfItsCapacity(self):
    server = Server(id="serverId", slot_capacity=4)
    vm1 = VirtualMachine(id="vmId", size=4)
    vm2 = VirtualMachine(id="vmId", size=1)

    assert_that(server.can_fit(vm1))
    assert_that(server.can_fit(vm2))

  def test_aServer_cannotFit_aVmBiggerThanItsCapacity(self):
    server = Server(id="serverId", slot_capacity=4)
    vm = VirtualMachine(id="vmId", size=5)

    assert_that(server.can_fit(vm), is_not(True))

  def test_aServerWithSomeLoad_canFitVms_smallerOrEqualOfTheRemainingSlots(self):
    server = Server(id="serverId", slot_capacity=10)
    vm1 = VirtualMachine(id="vmId", size=5)
    vm2 = VirtualMachine(id="vmId", size=3)

    server.add_vm(vm1)
    server.add_vm(vm2)

    vm3 = VirtualMachine(id="vmId", size=2)
    vm4 = VirtualMachine(id="vmId", size=1)
    assert_that(server.can_fit(vm3))
    assert_that(server.can_fit(vm4))

  def test_aServerWithALoad_cannotFitAVmBiggerThanRemainingSlots(self):
    server = Server(id="serverId", slot_capacity=10)
    vm1 = VirtualMachine(id="vmId", size=5)
    vm2 = VirtualMachine(id="vmId", size=3)

    server.add_vm(vm1)
    server.add_vm(vm2)

    vm3 = VirtualMachine(id="vmId", size=3)
    assert_that(server.can_fit(vm3), is_not(True))

  def test_addingVms_toAServer_changesItsCurrentLoadPercentage(self):
    server = Server(id="serverId", slot_capacity=10)

    vm1 = VirtualMachine(id="vmId", size=2)
    server.add_vm(vm1)
    assert_that(server.current_load_percentage, equal_to(20))

    vm2= VirtualMachine(id="vmId", size=3)
    server.add_vm(vm2)
    assert_that(server.current_load_percentage, equal_to(50))

    vm3 = VirtualMachine(id="vmId", size=4)
    server.add_vm(vm3)
    assert_that(server.current_load_percentage, equal_to(90))

  def test_currentLoadPercentageIsRounded_whenNeeded(self):
    server = Server(id="serverId", slot_capacity=9)

    vm1 = VirtualMachine(id="vmId", size=3)
    server.add_vm(vm1)
    assert_that(server.current_load_percentage, equal_to(33))

    vm2= VirtualMachine(id="vmId", size=3)
    server.add_vm(vm2)
    assert_that(server.current_load_percentage, equal_to(67))

if __name__ == '__main__':
  unittest.main()
