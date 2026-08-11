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
module: cp_mgmt_show_guideline_cells
short_description: Showing guideline-cells metrics according to the given filters.
description:
  - Showing guideline-cells metrics according to the given filters.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  guideline:
    description:
      - The guideline the user wish to view (identified by name or UID).
    type: str
    required: True
  access_layer:
    description:
      - The access layer context for the guideline metrics display.
        The access-layer must be attached to the guideline.
    type: dict
    required: True
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
  filters:
    description:
      - The filters are used to filter the cells and services that will be returned in the response.
        'any' value in both 'from' and 'to' filters will return the whole matrix.
    type: dict
    suboptions:
      from:
        description:
          - The source segment of the cell (identified by name or UID).
            In case the value is 'any', entire row will be returned. Relevant only for 'Network Group' type.
        type: str
      to:
        description:
          - The destination segment of the cell (identified by name or UID).
            In case the value is 'any', entire column will be returned. Relevant only for 'Network Group' type.
        type: str
      from_type:
        description:
          - The type of the segment in the 'from' axis.
        type: str
        choices: ['network group', 'internet', 'other']
      to_type:
        description:
          - The type of the segment in the 'to' axis.
        type: str
        choices: ['network group', 'internet', 'other']
      services:
        description:
          - The services that will be used while calculating the metrics (identified by name or UID).
        type: list
        elements: str
  show_count:
    description:
      - Set of metrics type. The rules categories to return in the response.
    type: list
    elements: str
  show_rules:
    description:
      - This field is used to control whether to show the rules paths in the response. This field should be set to true only when the 'from' and 'to'
        filters fields are not 'any'.
    type: bool
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: show-guideline-cells
  cp_mgmt_show_guideline_cells:
    access_layer:
      access_layer: Network
    details_level: uid
    guideline: Corporate policy
"""

RETURN = """
cp_mgmt_show_guideline_cells:
  description: The checkpoint show-guideline-cells output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        guideline=dict(type='str', required=True),
        access_layer=dict(type='dict', options=dict(
            access_layer=dict(type='str'),
            policy_package=dict(type='str'),
            details_level=dict(type='str', choices=['uid', 'standard', 'full']),
            domains_to_process=dict(type='list', elements='str')
        ), required=True),
        filters=dict(type='dict', options=dict(
            to=dict(type='str'),
            from_type=dict(type='str', choices=['network group', 'internet', 'other']),
            to_type=dict(type='str', choices=['network group', 'internet', 'other']),
            services=dict(type='list', elements='str')
        )),
        show_count=dict(type='list', elements='str'),
        show_rules=dict(type='bool'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full'])
    )
    argument_spec['filters']['options']['from'] = dict(type='str')
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "show-guideline-cells"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
