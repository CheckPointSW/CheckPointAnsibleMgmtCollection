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
module: cp_mgmt_set_best_practice
short_description: Edit an existing Best Practice using object name, uid or best practice id. Activate or deactivate the best practice and its relevant objects.
description:
  - Edit an existing Best Practice using object name, uid or best practice id. Activate or deactivate the best practice and its relevant objects.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  best_practice_id:
    description:
      - Best Practice ID.
    type: str
  name:
    description:
      - Best Practice Name.
    type: str
  active:
    description:
      - The activation status of the best practice.
    type: bool
  deactivation_comment:
    description:
      - The reason for deactivating the best practice.<br><font color="red">Required only if</font> active is set to false.
    type: str
  deactivation_expiration_date:
    description:
      - When the deactivation expires. Date and time represented in international ISO 8601 format. Relevant only if deactivation-mode is set to 'expire-on'.
    type: str
  deactivation_mode:
    description:
      - Whether the deactivation never expires or expires on a specific date.<br><font color="red">Required only if</font> active is set to false.
    type: str
    choices: ['never', 'expire-on']
  relevant_objects:
    description:
      - The relevant objects to activate or deactivate, each with its own deactivation settings. Supports the 'update' action only.
    type: dict
    suboptions:
      update:
        description:
          - Updates a value from a collection
        type: dict
        suboptions:
          name:
            description:
              - The name of the relevant object to update, as shown in the 'show-best-practice' reply. For a security gateway relevant object,
                this is the security gateway name; for an access rule relevant object, this is the layer name.
            type: str
          deactivation_comment:
            description:
              - The reason for deactivating the relevant object.<br><font color="red">Required only if</font> enabled is set to false.
            type: str
          deactivation_expiration_date:
            description:
              - When the deactivation expires. Date and time represented in international ISO 8601 format. Relevant only if deactivation-mode
                is set to 'expire-on'.
            type: str
          deactivation_mode:
            description:
              - Whether the deactivation never expires or expires on a specific date.<br><font color="red">Required only if</font> enabled is set to false.
            type: str
            choices: ['never', 'expire-on']
          enabled:
            description:
              - The activation status of the relevant object in the Compliance scan.
            type: bool
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  ignore_warnings:
    description:
      - Apply changes ignoring warnings.
    type: bool
  ignore_errors:
    description:
      - Apply changes ignoring errors. You won't be able to publish such a changes. If ignore-warnings flag was omitted - warnings will also be ignored.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: set-best-practice
  cp_mgmt_set_best_practice:
    best_practice_id: FW164
    relevant_objects:
      update:
        deactivation_comment: Gateway excluded from this check.
        deactivation_mode: never
        enabled: false
        name: gw1
"""

RETURN = """
cp_mgmt_set_best_practice:
  description: The checkpoint set-best-practice output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        best_practice_id=dict(type='str'),
        name=dict(type='str'),
        active=dict(type='bool'),
        deactivation_comment=dict(type='str'),
        deactivation_expiration_date=dict(type='str'),
        deactivation_mode=dict(type='str', choices=['never', 'expire-on']),
        relevant_objects=dict(type='dict', options=dict(
            update=dict(type='dict', options=dict(
                name=dict(type='str'),
                deactivation_comment=dict(type='str'),
                deactivation_expiration_date=dict(type='str'),
                deactivation_mode=dict(type='str', choices=['never', 'expire-on']),
                enabled=dict(type='bool')
            ))
        )),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "set-best-practice"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
