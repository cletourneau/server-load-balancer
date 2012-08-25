from operator import attrgetter

class ServerLoadBalancer(object):
  def __remove_servers_with_not_enough_capacity(self, servers, minimum_capacity):
    return [s for s in servers if s.available_slot_count() >= minimum_capacity]

  def __sort_servers_by_load(self, servers):
    return sorted(servers, key=attrgetter('current_load_percentage'))

  def __add_vm_on_first_server_if_any(self, vm, servers):
    if len(servers) > 0:
      servers[0].add_vm(vm)


  def balance(self, servers, virtual_machines):
    for vm in virtual_machines:
      servers_with_enough_capacity = self.__remove_servers_with_not_enough_capacity(servers, vm.size)
      servers_sorted_by_load = self.__sort_servers_by_load(servers_with_enough_capacity)

      self.__add_vm_on_first_server_if_any(vm, servers_sorted_by_load)
