#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage CheckPoint Firewall (c) 2019
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: cp_mgmt_set_cloud_license_gateway
short_description: Edit existing gateway license using name or uid.
description:
  - Edit existing gateway license using name or uid.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  gateway:
    description:
      - Security gateway name or UID to set.
    type: str
    required: True
  enable_auto_distribution:
    description:
      - Enable or disable auto distribution of cloud licenses for the specified gateway.
    type: bool
    required: True
  domain:
    description:
      - Domain name or UID for the gateway. Required when running from MDS context.
    type: str
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: set-cloud-license-gateway
  cp_mgmt_set_cloud_license_gateway:
    enable_auto_distribution: true
    gateway: Gateway_0.0.0.0
"""

RETURN = """
cp_mgmt_set_cloud_license_gateway:
  description: The checkpoint set-cloud-license-gateway output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        gateway=dict(type='str', required=True),
        enable_auto_distribution=dict(type='bool', required=True),
        domain=dict(type='str')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "set-cloud-license-gateway"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
