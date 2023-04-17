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
module: cp_mgmt_where_used
short_description: Searches for usage of the target object in other objects and rules.
description:
  - Searches for usage of the target object in other objects and rules.
  - All operations are performed over Web Services API.
version_added: "5.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  name:
    description:
      - Object name.
    type: str
  dereference_group_members:
    description:
      - Indicates whether to dereference "members" field by details level for every object in reply.
    type: bool
  show_membership:
    description:
      - Indicates whether to calculate and show "groups" field for every object in reply.
    type: bool
  async_response:
    description:
      - Run command in asynchronous mode and return task UID. Use show-task command to check the progress of the task.
    type: bool
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  domains_to_process:
    description:
      - Indicates which domains to process the commands on. It cannot be used with the details-level full, must be run from the System Domain only and
        with ignore-warnings true. Valid values are, CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.
    type: list
    elements: str
  indirect:
    description:
      - Search for indirect usage.
    type: bool
  indirect_max_depth:
    description:
      - Maximum nesting level during indirect usage search.
    type: int
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: where-used
  cp_mgmt_where_used:
    name: Host 1
"""

RETURN = """
cp_mgmt_where_used:
  description: The checkpoint where-used output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        name=dict(type='str'),
        dereference_group_members=dict(type='bool'),
        show_membership=dict(type='bool'),
        async_response=dict(type='bool'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        domains_to_process=dict(type='list', elements='str'),
        indirect=dict(type='bool'),
        indirect_max_depth=dict(type='int')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "where-used"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
