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
module: cp_mgmt_def_setting
short_description: Manages def-setting objects on Checkpoint over Web Services API
description:
  - Manages def-setting objects on Checkpoint devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  name:
    description:
      - Object name.
    type: str
    required: True
  data_type:
    description:
      - The data type of the setting. Defined when the object is created and cannot be changed afterwards.
    type: str
    choices: ['boolean', 'integer', 'string', 'list']
  assignments:
    description:
      - Assignments.
    type: list
    elements: dict
    suboptions:
      value:
        description:
          - The value of the setting.
        type: str
      description:
        description:
          - The description for this setting.
        type: str
      enabled:
        description:
          - If the setting is enabled.
        type: bool
      from_version:
        description:
          - The gateway version this setting applies from.
        type: str
        choices: ['earliest', 'latest', 'r77', 'r80', 'r81', 'r82']
      model:
        description:
          - The gateway model this setting applies to.
        type: str
        choices: ['all', 'quantum', 'spark']
      position:
        description:
          - The position of the setting.
        type: str
        choices: ['top', 'bottom', '1-1000']
      targets:
        description:
          - The Gateways or Clusters the assignment is applied to, identified by name or UID.
        type: list
        elements: str
      to_version:
        description:
          - The gateway version this setting applies to.
        type: str
        choices: ['earliest', 'latest', 'r77', 'r80', 'r81', 'r82']
  color:
    description:
      - Color of the object. Should be one of existing colors.
    type: str
    choices: ['aquamarine', 'black', 'blue', 'crete blue', 'burlywood', 'cyan', 'dark green', 'khaki', 'orchid', 'dark orange', 'dark sea green',
             'pink', 'turquoise', 'dark blue', 'firebrick', 'brown', 'forest green', 'gold', 'dark gold', 'gray', 'dark gray', 'light green', 'lemon chiffon',
             'coral', 'sea green', 'sky blue', 'magenta', 'purple', 'slate blue', 'violet red', 'navy blue', 'olive', 'orange', 'red', 'sienna', 'yellow']
  comments:
    description:
      - Comments string.
    type: str
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  tags:
    description:
      - Collection of tag identifiers.
    type: list
    elements: str
  ignore_warnings:
    description:
      - Apply changes ignoring warnings.
    type: bool
  ignore_errors:
    description:
      - Apply changes ignoring errors. You won't be able to publish such a changes. If ignore-warnings flag was omitted - warnings will also be ignored.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_objects
"""

EXAMPLES = """
- name: add-def-setting
  cp_mgmt_def_setting:
    assignments:
    - description: Default for Quantum gateways
      model: quantum
      value: 'true'
    - description: Default for Spark gateways
      model: spark
      value: 'false'
    data_type: boolean
    name: My Boolean Def Setting
    state: present

- name: set-def-setting
  cp_mgmt_def_setting:
    name: My Boolean Def Setting
    state: present

- name: delete-def-setting
  cp_mgmt_def_setting:
    name: My Boolean Def Setting
    state: absent
"""

RETURN = """
cp_mgmt_def_setting:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_objects, api_call


def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        data_type=dict(type='str', choices=['boolean', 'integer', 'string', 'list']),
        assignments=dict(type='list', elements='dict', options=dict(
            value=dict(type='str'),
            description=dict(type='str'),
            enabled=dict(type='bool'),
            from_version=dict(type='str', choices=['earliest', 'latest', 'r77', 'r80', 'r81', 'r82']),
            model=dict(type='str', choices=['all', 'quantum', 'spark']),
            position=dict(type='str', choices=['top', 'bottom', '1-1000']),
            targets=dict(type='list', elements='str'),
            to_version=dict(type='str', choices=['earliest', 'latest', 'r77', 'r80', 'r81', 'r82'])
        )),
        color=dict(type='str', choices=['aquamarine', 'black', 'blue', 'crete blue', 'burlywood', 'cyan', 'dark green',
                                        'khaki', 'orchid', 'dark orange', 'dark sea green', 'pink', 'turquoise', 'dark blue', 'firebrick', 'brown',
                                        'forest green', 'gold', 'dark gold', 'gray', 'dark gray', 'light green', 'lemon chiffon', 'coral', 'sea green',
                                        'sky blue', 'magenta', 'purple', 'slate blue', 'violet red', 'navy blue', 'olive', 'orange', 'red', 'sienna',
                                        'yellow']),
        comments=dict(type='str'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        tags=dict(type='list', elements='str'),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    api_call_object = 'def-setting'

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
