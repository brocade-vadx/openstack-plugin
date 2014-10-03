# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Brocade Communication Systems,Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Pattabi Ayyasami, Brocade Communications Systems,Inc.

from neutron.common import log
from neutron.services.loadbalancer.agent import agent_device_driver
from neutron.context import get_admin_context
from neutron.openstack.common import log as logging
from neutron import manager
from neutron.plugins.common import constants
from brocade_neutron_lbaas import (
    adx_device_driver_v1 as device_driver
)

DRIVER_NAME = 'brocade_agent_device_driver'
LOG = logging.getLogger(__name__)


class BrocadeAgentDeviceDriverV1(agent_device_driver.AgentDeviceDriver):
    """Abstract device driver that defines the API required by LBaaS agent."""

    def __init__(self, conf, plugin_rpc):
        self.plugin_rpc = plugin_rpc
        self.device_driver = None
        self.plugin = manager.NeutronManager.get_service_plugins()[
            constants.LOADBALANCER]
        self.device_driver = device_driver.BrocadeAdxDeviceDriverV1(self.plugin)

    def get_name(cls):
        """Returns unique name across all LBaaS device drivers."""
        return DRIVER_NAME

    def deploy_instance(self, logical_config):
        """Fully deploys a loadbalancer instance from a given config."""
        pass

    def undeploy_instance(self, pool_id):
        """Fully undeploys the loadbalancer instance."""
        pass

    def get_stats(self, pool_id):
        self.device_driver.get_pool_stats(pool_id)

    def remove_orphans(self, known_pool_ids):
        # Not all drivers will support this
        raise NotImplementedError()

    @log.log
    def create_vip(self, vip):
        self.device_driver.create_vip(vip)

    @log.log
    def update_vip(self, old_vip, vip):
        self.device_driver.update_vip(vip, old_vip)

    @log.log
    def delete_vip(self, vip):
        self.device_driver.delete_vip(vip)

    @log.log
    def create_pool(self, pool):
        self.device_driver.create_pool(pool)

    @log.log
    def update_pool(self, old_pool, pool):
        self.device_driver.update_pool(pool, old_pool)

    @log.log
    def delete_pool(self, pool):
        self.device_driver.delete_pool(pool)

    @log.log
    def create_member(self, member):
        self.device_driver.create_member(member)

    @log.log
    def update_member(self, old_member, member):
        self.device_driver.update_member(member, old_member)

    @log.log
    def delete_member(self, member):
        self.device_driver.delete_member(member)

    @log.log
    def create_pool_health_monitor(self, health_monitor, pool_id):
        self.device_driver.create_health_monitor(health_monitor,
                                                 pool_id)

    @log.log
    def update_pool_health_monitor(self,
                                   old_health_monitor,
                                   health_monitor,
                                   pool_id):
        self.device_driver.update_health_monitor(health_monitor,
                                                 old_health_monitor,
                                                 pool_id)

    @log.log
    def delete_pool_health_monitor(self, health_monitor, pool_id):
        self.device_driver.delete_health_monitor(health_monitor,
                                                 pool_id)
