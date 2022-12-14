# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"

  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  config.vm.hostname = "django-chat.test"
  config.hostsupdater.remove_on_suspend = true

  config.vm.synced_folder ".", "/vagrant", type: "nfs", nfs_version: 4.2, nfs_udp: false

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048
    vb.name = "django_chat"
  end

  config.vm.provision "shell", path: "./django_chat/setup.sh"
end
