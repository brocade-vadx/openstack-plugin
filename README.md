This repository contains the Brocade LBaaS Plugin Driver code for OpenStack. 

Pre-requisites
--------------
- Install Brocade Neutron LBaaS Device Driver 
    
    - Please refer to https://github.com/brocade-vadx/adx-device-driver for details

Install Instructions
--------------------
- Download and install the Brocade LBaaS Plugin Driver code

    - From a temporary location, run "git clone https://github.com/brocade-vadx/openstack-plugin.git"

    - Change directory ("cd openstack-plugin")

    - Create $NEUTRON_HOME/services/loadbalancer/drivers/brocade directory if it does not exist

    - Copy the contents ("sudo cp * $NEUTRON_HOME/services/loadbalancer/drivers/brocade/") to $NEUTRON_HOME/services/loadbalancer/drivers/brocade directory. 

    - $NEUTRON_HOME) is the location where OpenStack neutron component is installed. For example, $NEUTRON_HOME could be /usr/local/lib/python2.7/dist-packages/neutron

    - Enable the Brocade LBaaS Plugin Driver in neutron.conf

    - comment the Haproxy (which is the default service provider for LOADBALANCER) under service_provider section and specify Brocade as the service provider for LOADBALANCER (as shown below)

    - service_provider = LOADBALANCER:brocade:neutron.services.loadbalancer.drivers.brocade.plugin_driver_v1.BrocadePluginDriverV1:default

    - Restart OpenStack Neutron Server
