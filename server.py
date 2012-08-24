class Server(object):
  def __init__(self, id, slot_capacity):
    self.id = id
    self.slot_capacity = slot_capacity
    self.vms = []
    self.current_load_percentage = 0

  def __computeLoad(self):
    all_vms_size = 0
    for vm in self.vms: all_vms_size += vm.size
    percentage = (float(all_vms_size) / float(self.slot_capacity)) * 100.0
    self.current_load_percentage = int(round(percentage, 0))

  def addVm(self, vm):
    self.vms.append(vm)
    self.__computeLoad()
