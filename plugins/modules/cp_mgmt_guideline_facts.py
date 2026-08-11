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
module: cp_mgmt_guideline_facts
short_description: Get guideline objects facts on Checkpoint over Web Services API
description:
  - Get guideline objects facts on Checkpoint devices.
  - All operations are performed over Web Services API.
  - This module handles both operations, get a specific object and get several objects,
    For getting a specific object use the parameter 'name'.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  name:
    description:
      - Object name.
        This parameter is relevant only for getting a specific object.
    type: str
  show_indexing_status:
    description:
      - Control whether to show the indexing status of the guideline.
    type: bool
  indexing_status_layer:
    description:
      - Relevant only when show-indexing-status is true. The access-layer to show the indexing status of (identified by unique id or 'any' for all
        attached access-layers).
    type: str
  dereference_group_members:
    description:
      - Indicates whether to dereference "members" field by details level for every object in reply.
    type: bool
  show_membership:
    description:
      - Indicates whether to calculate and show "groups" field for every object in reply.
    type: bool
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  filter:
    description:
      - Additional filters for the query.
    type: dict
    suboptions:
      access_layers:
        description:
          - List of access-layers identifiers to filter by. The query will return only guidelines that are attached to the given access-layers.
        type: list
        elements: str
      layer_with_policy:
        description:
          - List of access-layer and policy-package pairs to filter by. For global access-layers, both access-layer and policy-package must match.
            For local access-layers, only the access-layer needs to match.
        type: list
        elements: dict
        suboptions:
          access_layer:
            description:
              - Access-layer attached to guideline identified by the name or UID.if Access-Layer is in the global domain due to Global
                Assignment Local domain Package is required.
            type: str
          policy_package:
            description:
              - Policy package context for the access-layer attached to guideline identified by the name or UID.Package will be ignored if the
                access-layer is local.
            type: str
          details_level:
            description:
              - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully
                detailed representation of the object.
            type: str
            choices: ['uid', 'standard', 'full']
          domains_to_process:
            description:
              - Indicates which domains to process the commands on. It cannot be used with the details-level full, must be run from the System
                Domain only and with ignore-warnings true. Valid values are, CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.
            type: list
            elements: str
      query:
        description:
          - Search expression to filter objects by. The provided text should be exactly the same as it would be given in SmartConsole Object
            Explorer. The logical operators in the expression ('AND', 'OR') should be provided in capital letters. The search involves both a IP search and a
            textual search in name, comment, tags etc.
        type: str
      policy_packages:
        description:
          - List of local-domain policy packages identifiers to filter by, in case a guideline is attached to a layer with assigned global policy.
        type: str
  limit:
    description:
      - The maximal number of returned results.
        This parameter is relevant only for getting few objects.
    type: int
  offset:
    description:
      - Number of the results to initially skip.
        This parameter is relevant only for getting few objects.
    type: int
  order:
    description:
      - Sorts the results by search criteria. Automatically sorts the results by Name, in the ascending order.
        This parameter is relevant only for getting few objects.
    type: list
    elements: dict
    suboptions:
      ASC:
        description:
          - Sorts results by the given field in ascending order.
        type: str
        choices: ['name']
      DESC:
        description:
          - Sorts results by the given field in descending order.
        type: str
        choices: ['name']
  domains_to_process:
    description:
      - Indicates which domains to process the commands on. It cannot be used with the details-level full, must be run from the System Domain only and
        with ignore-warnings true. Valid values are, CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.
    type: list
    elements: str
  show_only_local_domain:
    description:
      - Indicates whether the query should return only objects from the current local domain. This parameter is only valid for local domain.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_facts
"""

EXAMPLES = """
- name: show-guideline
  cp_mgmt_guideline_facts:
    name: Corporate policy

- name: show-guidelines
  cp_mgmt_guideline_facts:
"""

RETURN = """
ansible_facts:
  description: The checkpoint object facts.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_facts, api_call_facts


def main():
    argument_spec = dict(
        name=dict(type='str'),
        show_indexing_status=dict(type='bool'),
        indexing_status_layer=dict(type='str'),
        dereference_group_members=dict(type='bool'),
        show_membership=dict(type='bool'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        filter=dict(type='dict', options=dict(
            access_layers=dict(type='list', elements='str'),
            layer_with_policy=dict(type='list', elements='dict', options=dict(
                access_layer=dict(type='str'),
                policy_package=dict(type='str'),
                details_level=dict(type='str', choices=['uid', 'standard', 'full']),
                domains_to_process=dict(type='list', elements='str')
            )),
            query=dict(type='str'),
            policy_packages=dict(type='str')
        )),
        limit=dict(type='int'),
        offset=dict(type='int'),
        order=dict(type='list', elements='dict', options=dict(
            ASC=dict(type='str', choices=['name']),
            DESC=dict(type='str', choices=['name'])
        )),
        domains_to_process=dict(type='list', elements='str'),
        show_only_local_domain=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_facts)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    api_call_object = "guideline"
    api_call_object_plural_version = "guidelines"

    result = api_call_facts(module, api_call_object, api_call_object_plural_version)
    module.exit_json(ansible_facts=result)


if __name__ == '__main__':
    main()
