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
module: cp_mgmt_gaia_api
short_description: Runs a gaia-api command from the management. 
description:
  - Runs a gaia-api command from the management. 
Syntax: gaia-api/gateway-command. Gateway-command is the gaia-api command which you want to send the request. Please take a look at the examples to know how
to use it. Please include any input parameters needed in the request body.
 The cache config file in $FWDIR/api/conf/cache.conf can be used to change the settings.
NOTE: Please add a rule to allow the connection from the management to the targets.
  - All operations are performed over Web Services API.
version_added: "6.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  target:
    description:
      - Gateway-object-name or gateway-ip-address or gateway-UID.
    type: str
  other_parameter:
    description:
      - Other input parameters that gateway needs it.
    type: str
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: gaia-api
  cp_mgmt_gaia_api:
    target: 52048978-c507-8243-9d84-074d11154616
"""

RETURN = """
cp_mgmt_gaia_api:
  description: The checkpoint gaia-api output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        target=dict(type='str'),
        other_parameter=dict(type='str')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "gaia-api"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
