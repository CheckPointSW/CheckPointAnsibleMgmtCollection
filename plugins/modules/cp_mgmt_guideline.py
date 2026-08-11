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
module: cp_mgmt_guideline
short_description: Manages guideline objects on Checkpoint over Web Services API
description:
  - Manages guideline objects on Checkpoint devices including creating, updating and removing objects.
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
  access_layers:
    description:
      - Collection of access-layers (one or more) of the guideline, identified by name or UID.
    type: list
    elements: dict
    suboptions:
      access_layer:
        description:
          - Access-layer attached to guideline identified by the name or UID.if Access-Layer is in the global domain due to Global Assignment
            Local domain Package is required.
        type: str
      policy_package:
        description:
          - Policy package context for the access-layer attached to guideline identified by the name or UID.Package will be ignored if the
            access-layer is local.
        type: str
      details_level:
        description:
          - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
            representation of the object.
        type: str
        choices: ['uid', 'standard', 'full']
      domains_to_process:
        description:
          - Indicates which domains to process the commands on. It cannot be used with the details-level full, must be run from the System Domain
            only and with ignore-warnings true. Valid values are, CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.
        type: list
        elements: str
  guideline_groups:
    description:
      - Collection of segments of the guideline.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Network group name.
        type: str
      position:
        description:
          - Guideline-Group Position in the guideline. If a position is specified for one guideline-group, it is required for all guideline-groups.
        type: str
  cell_actions_override:
    description:
      - Cells that their action will override the default actions of the guideline.
    type: list
    elements: dict
    suboptions:
      from:
        description:
          - The segment identifier (name or UID) of the cell in the 'from' axis. The field is mandatory only if "from-type" is "network group".
        type: str
      from_type:
        description:
          - The type of the segment in the 'from' axis.
        type: str
        choices: ['network group', 'internet', 'other']
      to:
        description:
          - The segment identifier (name or UID) of the cell in the 'to' axis. The field is mandatory only if "to-type" is "network group".
        type: str
      to_type:
        description:
          - The type of the segment in the 'to' axis.
        type: str
        choices: ['network group', 'internet', 'other']
      action:
        description:
          - The action to be applied to the cell. The field is mandatory at add command.
        type: str
        choices: ['All traffic is allowed', 'All traffic is not allowed', 'Decide later']
      allowed_services:
        description:
          - Services (identified by name or UID) that are allowed in the cell. Relevant only if the action in the cell is 'All traffic is not
            allowed'. To remove allowed-services call update with the same "All traffic is not allowed" action, or remove the cell-action-override.
        type: list
        elements: str
  dereference_group_members:
    description:
      - Indicates whether to dereference "members" field by details level for every object in reply.
    type: bool
  show_membership:
    description:
      - Indicates whether to calculate and show "groups" field for every object in reply.
    type: bool
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
- name: add-guideline
  cp_mgmt_guideline:
    access_layers:
    - Network
    guideline_groups:
    - name: DMZ
    - name: Users networks
    - name: Labs
    name: Corporate policy
    state: present

- name: set-guideline
  cp_mgmt_guideline:
    name: Corporate policy
    state: present

- name: delete-guideline
  cp_mgmt_guideline:
    name: Corporate policy
    state: absent
"""

RETURN = """
cp_mgmt_guideline:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_objects, api_call


def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        access_layers=dict(type='list', elements='dict', options=dict(
            access_layer=dict(type='str'),
            policy_package=dict(type='str'),
            details_level=dict(type='str', choices=['uid', 'standard', 'full']),
            domains_to_process=dict(type='list', elements='str')
        )),
        guideline_groups=dict(type='list', elements='dict', options=dict(
            name=dict(type='str'),
            position=dict(type='str')
        )),
        cell_actions_override=dict(type='list', elements='dict', options=dict(
            from_type=dict(type='str', choices=['network group', 'internet', 'other']),
            to=dict(type='str'),
            to_type=dict(type='str', choices=['network group', 'internet', 'other']),
            action=dict(type='str', choices=['All traffic is allowed', 'All traffic is not allowed', 'Decide later']),
            allowed_services=dict(type='list', elements='str')
        )),
        dereference_group_members=dict(type='bool'),
        show_membership=dict(type='bool'),
        color=dict(type='str', choices=['aquamarine', 'black', 'blue', 'crete blue', 'burlywood', 'cyan', 'dark green',
                                        'khaki', 'orchid', 'dark orange', 'dark sea green', 'pink', 'turquoise', 'dark blue', 'firebrick', 'brown',
                                        'forest green', 'gold', 'dark gold', 'gray', 'dark gray', 'light green', 'lemon chiffon', 'coral', 'sea green',
                                        'sky blue', 'magenta', 'purple', 'slate blue', 'violet red', 'navy blue', 'olive', 'orange', 'red', 'sienna',
                                        'yellow']),
        comments=dict(type='str'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool')
    )
    argument_spec['cell_actions_override']['options']['from'] = dict(type='str')
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    api_call_object = 'guideline'

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
