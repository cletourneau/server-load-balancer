from operator import attrgetter

class ServerLoadBalancer(object):
  def __remove_servers_with_not_enough_capacity(self, servers, vm):
    return [s for s in servers if s.can_fit(vm)]

  def __sort_servers_by_load_percentage(self, servers):
    return sorted(servers, key=attrgetter('current_load_percentage'))

  def balance(self, servers, virtual_machines):
    for vm in virtual_machines:
      servers_big_enough = self.__remove_servers_with_not_enough_capacity(servers, vm)

      if servers_big_enough:
        sorted_servers = self.__sort_servers_by_load_percentage(servers_big_enough)
        sorted_servers[0].add_vm(vm)
