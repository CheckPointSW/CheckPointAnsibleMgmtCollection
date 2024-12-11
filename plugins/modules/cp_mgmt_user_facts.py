#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: cp_mgmt_user_facts
short_description: Get user objects facts on Checkpoint over Web Services API
description:
  - Get user objects facts on Checkpoint devices.
  - All operations are performed over Web Services API.
  - This module handles both operations, get a specific object and get several objects,
    For getting a specific object use the parameter 'name'.
version_added: "xxx"
author: "Christoph Spatt (@edeka-spatt)"
options:
  name:
    description:
      - Object name.
        This parameter is relevant only for getting a specific object.
    type: str
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  filter:
    description:
      - Search expression to filter objects by. The provided text should be exactly the same as it would be given in SmartConsole Object Explorer. The
        logical operators in the expression ('AND', 'OR') should be provided in capital letters. The search involves both a IP search and a textual search in
        name, comment, tags etc.
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
extends_documentation_fragment: check_point.mgmt.checkpoint_facts
"""

EXAMPLES = """
- name: show-user
  cp_mgmt_user_facts:
    name: myusergroup

- name: show-users
  cp_mgmt_user_facts:
    details_level: full
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
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        filter=dict(type='str'),
        limit=dict(type='int'),
        offset=dict(type='int'),
        order=dict(type='list', elements='dict', options=dict(
            ASC=dict(type='str', choices=['name']),
            DESC=dict(type='str', choices=['name'])
        ))
    )
    argument_spec.update(checkpoint_argument_spec_for_facts)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    api_call_object = "user"
    api_call_object_plural_version = "users"

    result = api_call_facts(module, api_call_object, api_call_object_plural_version)
    module.exit_json(ansible_facts=result)


if __name__ == '__main__':
    main()
