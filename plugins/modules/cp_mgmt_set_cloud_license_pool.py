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
module: cp_mgmt_set_cloud_license_pool
short_description: Edit existing pool using name.
description:
  - Edit existing pool using name.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  pool:
    description:
      - Pool name.
    type: str
    required: True
  ck:
    description:
      - Contract Key. Required to identify a specific pool when multiple pools share the same name.
    type: str
  default_pool:
    description:
      - Set pool to default. This value can only be changed from false to true. To disable the current default pool, you must set a different pool as
        the default.
    type: bool
    choices: ['true']
  migrate_gateways:
    description:
      - Move gateways from current default pool to the new default pool. Required when default-pool parameter is set to true.
    type: bool
  assigned_gateways:
    description:
      - Attach security gateways to the pool. The attached gateways will use licenses from this pool.
    type: list
    elements: dict
    suboptions:
      gateway:
        description:
          - Gateway name or uid.
        type: str
      domain:
        description:
          - Domain name or uid. Required when running from MDS context.
        type: str
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: set-cloud-license-pool
  cp_mgmt_set_cloud_license_pool:
    assigned_gateways:
    - gateway: GW_A
    - gateway: GW_B
    pool: VE-NGTX
"""

RETURN = """
cp_mgmt_set_cloud_license_pool:
  description: The checkpoint set-cloud-license-pool output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        pool=dict(type='str', required=True),
        ck=dict(type='str'),
        default_pool=dict(type='bool', choices=['true']),
        migrate_gateways=dict(type='bool'),
        assigned_gateways=dict(type='list', elements='dict', options=dict(
            gateway=dict(type='str'),
            domain=dict(type='str')
        ))
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "set-cloud-license-pool"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
