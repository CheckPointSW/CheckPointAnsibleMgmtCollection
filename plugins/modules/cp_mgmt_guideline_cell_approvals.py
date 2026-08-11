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
module: cp_mgmt_guideline_cell_approvals
short_description: Manages guideline-cell-approvals objects on Checkpoint over Web Services API
description:
  - Manages guideline-cell-approvals objects on Checkpoint devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  guideline:
    description:
      - The guideline (identified by UID or name) in which we approve the violation.
    type: str
  approvals:
    description:
      - List of approved rules.
    type: list
    elements: dict
    suboptions:
      rules:
        description:
          - The full paths (pairs of layer and rule) of the approved rules.
        type: list
        elements: dict
        suboptions:
          layer:
            description:
              - The Layer identifier (name or UID).
            type: str
          rule:
            description:
              - The rule identifier (name if unique, rule position number in rule-base or UID).
            type: str
  from:
    description:
      - a "from" segment (identified by UID or name), or 'any' to approved the rule across all cells (possible only if "to" is also 'any'). This field
        is mandatory if "from-type" is 'Network Group'.
    type: str
  from_type:
    description:
      - The type of the segment in the 'from' axis.
    type: str
    choices: ['network group', 'internet', 'other']
  to:
    description:
      - a "to" segment (identified by UID or name), or 'any' to approved the rule across all cells (possible only if "from" is also 'any'). This field
        is mandatory if "to-type" is 'Network Group'.
    type: str
  to_type:
    description:
      - The type of the segment in the 'to' axis.
    type: str
    choices: ['network group', 'internet', 'other']
  comment:
    description:
      - New comment for the approvals. The same comment to all the requested approvals.
    type: str
  policy_package:
    description:
      - The policy package (identified by UID or name) in which we approve the violation. This field is mandatory only if the ordered-access-layer
        (first layer in path) is from a global domain with AGP.
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
  delete_scope:
    description:
      - Indicates whether to delete all the approval scope, or only remove the requested cell from the scope. Relevant only for guideline approvals.
    type: str
    choices: ['single cell', 'effected cells', 'guideline']
extends_documentation_fragment: check_point.mgmt.checkpoint_objects
"""

EXAMPLES = """
- name: add-guideline-cell-approvals
  cp_mgmt_guideline_cell_approvals:
    comment: This is approved for all segments
    from: any
    guideline: Corporate policy
    state: present
    to: any

- name: set-guideline-cell-approvals
  cp_mgmt_guideline_cell_approvals:
    comment: This is approved for all segments, including future
    from: any
    guideline: Corporate policy
    state: present
    to: any

- name: delete-guideline-cell-approvals
  cp_mgmt_guideline_cell_approvals:
    from: any
    guideline: Corporate policy
    state: absent
    to: any
"""

RETURN = """
cp_mgmt_guideline_cell_approvals:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_objects, api_call


def main():
    argument_spec = dict(
        guideline=dict(type='str'),
        approvals=dict(type='list', elements='dict', options=dict(
            rules=dict(type='list', elements='dict', options=dict(
                layer=dict(type='str'),
                rule=dict(type='str')
            ))
        )),
        from_type=dict(type='str', choices=['network group', 'internet', 'other']),
        to=dict(type='str'),
        to_type=dict(type='str', choices=['network group', 'internet', 'other']),
        comment=dict(type='str'),
        policy_package=dict(type='str'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool'),
        delete_scope=dict(type='str', choices=['single cell', 'effected cells', 'guideline'])
    )
    argument_spec['from'] = dict(type='str')
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    api_call_object = 'guideline-cell-approvals'

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
