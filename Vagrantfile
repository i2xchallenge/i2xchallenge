# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANT_API_VERSION = "2"
Vagrant.configure(VAGRANT_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"

  # Provision using shell
  config.vm.host_name = "dev.i2x"
  config.vm.synced_folder ".", "/opt/i2x"
  config.vm.provision "shell", path: "scripts/vagrant-provision"

  # Networking details
  config.vm.network "forwarded_port", guest: 9000, host: 9000
  config.vm.network "private_network", ip: "172.28.128.4"
end
