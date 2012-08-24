class ServerLoadBalancer(object):
  def balance(self, servers, virtual_machines):
    if len(servers) > 0:
      for vm in virtual_machines:
        servers[0].addVm(vm)
