class Server(object):
  def __init__(self, id, slot_capacity):
    self.id = id
    self.slot_capacity = slot_capacity
    self.vms = []
    self.current_load_percentage = 0

  def __current_slot_usage(self):
    slot_usage = 0
    for vm in self.vms: slot_usage += vm.size
    return slot_usage

  def __compute_load(self):
    slot_usage = self.__current_slot_usage()
    percentage = (float(slot_usage) / float(self.slot_capacity)) * 100.0
    self.current_load_percentage = int(round(percentage, 0))

  def available_slot_count(self):
    return self.slot_capacity - self.__current_slot_usage()

  def add_vm(self, vm):
    self.vms.append(vm)
    self.__compute_load()
