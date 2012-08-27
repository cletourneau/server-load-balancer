class Server(object):
  def __init__(self, id, slot_capacity):
    self.id = id
    self.slot_capacity = slot_capacity
    self.vms = []
    self.current_load_percentage = 0
    self.__current_slot_usage = 0

  def __compute_load(self):
    percentage = (float(self.__current_slot_usage) / float(self.slot_capacity)) * 100.0
    self.current_load_percentage = int(round(percentage, 0))

  def can_fit(self, vm):
    available_slot_count = self.slot_capacity - self.__current_slot_usage
    return available_slot_count >= vm.size

  def add_vm(self, vm):
    self.vms.append(vm)
    self.__current_slot_usage += vm.size
    self.__compute_load()
