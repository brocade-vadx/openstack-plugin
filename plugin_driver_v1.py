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
from neutron.db.loadbalancer import loadbalancer_db
from neutron.openstack.common import log as logging
from neutron.plugins.common import constants
from neutron.services.loadbalancer.drivers import abstract_driver
from brocade_neutron_lbaas import (
    adx_device_driver_v1 as device_driver
)

LOG = logging.getLogger(__name__)

class BrocadePluginDriverV1(abstract_driver.LoadBalancerAbstractDriver):

    """Brocade LBAAS Plugin Driver."""

    def __init__(self, plugin):
        LOG.debug(_('Initializing Brocade Load Balancer Plugin Driver'))
        self.plugin = plugin
        self.db = loadbalancer_db.LoadBalancerPluginDb()
        self.device_driver = device_driver.BrocadeAdxDeviceDriverV1(plugin)

    def _is_update_allowed(self, obj):
        return obj['status'] in [constants.ACTIVE]

    def active(self, context, model, id):
        self.db.update_status(context, model, id,
                              constants.ACTIVE)

    def error(self, context, model, id, status_description=None):
        self.db.update_status(context, model, id,
                              constants.ERROR,
                              status_description)

    @log.log
    def create_vip(self, context, vip):
        try:
            self.device_driver.create_vip(vip)
            self.active(context, loadbalancer_db.Vip, vip["id"])
        except Exception as e:
            LOG.error(_("Exception in create_vip in device driver : %s"), e)
            self.error(context, loadbalancer_db.Vip, vip["id"], e.msg)

    @log.log
    def update_vip(self, context, old_vip, new_vip):
        try:
            self.device_driver.update_vip(new_vip, old_vip)
            self.active(context, loadbalancer_db.Vip, new_vip["id"])
        except Exception as e:
            LOG.error(_("Exception in update_vip in device driver : %s"), e)
            self.error(context, loadbalancer_db.Vip, new_vip["id"], e.msg)

    @log.log
    def delete_vip(self, context, vip):
        try:
            self.device_driver.delete_vip(vip)
        except Exception as e:
            LOG.error(_("Exception in delete_vip in device driver : %s"), e)

        # Delete VIP from DB any case
        self.plugin._delete_db_vip(context, vip["id"])

    @log.log
    def create_pool(self, context, pool):
        try:
            self.device_driver.create_pool(pool)
            self.active(context, loadbalancer_db.Pool, pool["id"])
        except Exception as e:
            LOG.error(_("Exception in create_pool in device driver : %s"), e)
            #self.error(context, loadbalancer_db.Pool, pool["id"], e.msg)

    @log.log
    def update_pool(self, context, old_pool, new_pool):
        try:
            self.device_driver.update_pool(new_pool, old_pool)
            self.active(context, loadbalancer_db.Pool, new_pool["id"])
        except Exception as e:
            LOG.error(_("Exception in update in device driver : %s"), e)
            self.error(context, loadbalancer_db.Pool, new_pool["id"], e.msg)

    @log.log
    def delete_pool(self, context, pool):
        try:
            self.device_driver.delete_pool(pool)
        except Exception as e:
            LOG.error(_("Exception in delete_pool in device driver : %s"), e)

        # Delete Pool from DB any case
        self.plugin._delete_db_pool(context, pool['id'])

    @log.log
    def stats(self, context, pool_id):
        self.device_driver.get_pool_stats(pool_id)

    @log.log
    def create_member(self, context, member):
        try:
            # call the device driver api
            self.device_driver.create_member(member)
            self.active(context, loadbalancer_db.Member, member["id"])
        except Exception as e:
            LOG.error(_("Exception in create_member in device driver : %s"), e)
            self.error(context, loadbalancer_db.Member, member["id"], e.msg)

    @log.log
    def update_member(self, context, old_member, new_member):
        try:
            self.device_driver.update_member(new_member, old_member)
            self.active(context, loadbalancer_db.Member, new_member["id"])
        except Exception as e:
            LOG.error(_("Exception in update_member in device driver : %s"), e)
            self.error(context, loadbalancer_db.Member,
                       new_member["id"], e.msg)

    @log.log
    def delete_member(self, context, member):
        try:
            self.device_driver.delete_member(member)
        except Exception as e:
            LOG.error(_("Exception in delete_member in device driver : %s"), e)

        # Delete Member from DB any case
        self.plugin._delete_db_member(context, member["id"])

    @log.log
    def update_pool_health_monitor(self, context, old_health_monitor,
                              new_health_monitor,
                              pool_id):
        try:
            self.device_driver.update_health_monitor(new_health_monitor,
                                                     old_health_monitor,
                                                     pool_id)
            self.db.update_pool_health_monitor(context,
                                               new_health_monitor['id'],
                                               pool_id,
                                               constants.ACTIVE)
        except Exception as e:
            LOG.error(_("Exception in update_health_monitor "
                        "in device driver : %s"), e)
            self.db.update_pool_health_monitor(context,
                                               new_health_monitor['id'],
                                               pool_id,
                                               constants.ERROR,
                                               e.msg)

    @log.log
    def create_pool_health_monitor(self, context, health_monitor, pool_id):
        try:
            self.device_driver.create_health_monitor(health_monitor,
                                                     pool_id)
            self.db.update_pool_health_monitor(context,
                                               health_monitor['id'],
                                               pool_id,
                                               constants.ACTIVE)
        except Exception as e:
            LOG.error(_("Exception in create_health_monitor "
                        "in device driver : %s"), e)
            self.db.update_pool_health_monitor(context,
                                               health_monitor['id'],
                                               pool_id,
                                               constants.ERROR,
                                               e.msg)

    @log.log
    def delete_pool_health_monitor(self, context, health_monitor, pool_id):
        try:
            self.device_driver.delete_health_monitor(health_monitor,
                                                     pool_id)
        except Exception as e:
            LOG.error(_("Exception in delete_health_monitor "
                        "in device driver : %s"), e)

        self.plugin._delete_db_pool_health_monitor(context,
                                                   health_monitor["id"],
                                                   pool_id)
