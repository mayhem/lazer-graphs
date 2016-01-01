# -*- mode: ruby -*-
# vi: set ft=ruby :

hosts = [
  { name: 'graphs', memory: '512' }
]

Vagrant.configure("2") do |config|
  hosts.each do |host|
    config.vm.define host[:name] do |c|
      c.vm.box = "ubuntu/trusty64"
      c.vm.hostname = host[:name]
      c.vm.network "forwarded_port", guest: 8000, host: 8000
      c.vm.provider :virtualbox do |vb|
        modifyvm_args = ['modifyvm', :id]
        modifyvm_args << "--memory" << host[:memory]
        modifyvm_args << "--name" << host[:name]
        modifyvm_args << "--natdnsproxy1" << "on"
        modifyvm_args << "--natdnshostresolver1" << "on"
        vb.customize(modifyvm_args)
      end
      c.vm.provision :shell, :path => "bootstrap.sh"
      c.vm.synced_folder ".", "/home/vagrant/lazer-graphs"
    end
  end
end
