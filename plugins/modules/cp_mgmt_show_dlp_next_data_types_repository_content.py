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
module: cp_mgmt_show_dlp_next_data_types_repository_content
short_description: Retrieve all DLP Next Data Type Objects from Infinity portal.
description:
  - Retrieve all DLP Next Data Type Objects from Infinity portal.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  filter:
    description:
      - Filter by object name in repository.
    type: str
  limit:
    description:
      - The maximal number of returned results.
    type: int
  offset:
    description:
      - Number of the results to initially skip.
    type: int
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  show_only_local_domain:
    description:
      - Indicates whether the query should return only objects from the current local domain. This parameter is only valid for local domain.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: show-dlp-next-data-types-repository-content
  cp_mgmt_show_dlp_next_data_types_repository_content:
    limit: 1
"""

RETURN = """
cp_mgmt_show_dlp_next_data_types_repository_content:
  description: The checkpoint show-dlp-next-data-types-repository-content output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        filter=dict(type='str'),
        limit=dict(type='int'),
        offset=dict(type='int'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        show_only_local_domain=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "show-dlp-next-data-types-repository-content"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
