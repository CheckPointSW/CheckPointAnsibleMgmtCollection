#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Ansible module to manage Check Point Firewall (c) 2019
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
module: cp_mgmt_access_role
short_description: Manages access-role objects on Check Point over Web Services API
description:
  - Manages access-role objects on Check Point devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
version_added: "1.0.0"
author: "Or Soffer (@chkp-orso)"
options:
  name:
    description:
      - Object name.
    type: str
    required: True
  machines_list:
    description:
      - Machines that can access the system.
    type: list
    elements: dict
    suboptions:
      source:
        description:
          - Active Directory name or UID or Identity Tag.
        type: str
      selection:
        description:
          - Name or UID of an object selected from source.
        type: list
        elements: str
      base_dn:
        description:
          - When source is "Active Directory" use "base-dn" to refine the query in AD database.
        type: str
  machines:
    description:
      - Any or All Identified.
    type: str
    choices: ['any', 'all identified']
  networks:
    description:
      - Collection of Network objects identified by the name or UID that can access the system.
    type: list
    elements: str
  remote_access_clients:
    description:
      - Remote access clients identified by name or UID.
    type: str
  tags:
    description:
      - Collection of tag identifiers.
    type: list
    elements: str
  users_list:
    description:
      - Users that can access the system.
    type: list
    elements: dict
    suboptions:
      source:
        description:
          - Active Directory name or UID or Identity Tag  or Internal User Groups or LDAP groups or Guests.
        type: str
      selection:
        description:
          - Name or UID of an object selected from source.
        type: list
        elements: str
      base_dn:
        description:
          - When source is "Active Directory" use "base-dn" to refine the query in AD database.
        type: str
  users:
    description:
      - Any or All Identified.
    type: str
    choices: ['any', 'all identified']
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
- name: add-access-role
  cp_mgmt_access_role:
    name: New Access Role 1
    networks: any
    remote_access_clients: any
    state: present
    users: any

- name: set-access-role
  cp_mgmt_access_role:
    users_list:
        - source: "Internal User Groups"
          selection: usersGroup
    name: New Access Role 1
    state: present

- name: delete-access-role
  cp_mgmt_access_role:
    name: New Access Role 1
    state: absent
"""

RETURN = """
cp_mgmt_access_role:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_objects, api_call


def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        machines_list=dict(type='list', elements='dict', options=dict(
            source=dict(type='str'),
            selection=dict(type='list', elements='str'),
            base_dn=dict(type='str')
        )),
        machines=dict(type='str', choices=['any', 'all identified']),
        networks=dict(type='list', elements='str'),
        remote_access_clients=dict(type='str'),
        tags=dict(type='list', elements='str'),
        users_list=dict(type='list', elements='dict', options=dict(
            source=dict(type='str'),
            selection=dict(type='list', elements='str'),
            base_dn=dict(type='str')
        )),
        users=dict(type='str', choices=['any', 'all identified']),
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
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    api_call_object = 'access-role'

    if module.params["machines_list"] is not None:
        if module.params["machines"] is not None:
            raise AssertionError("The use of both 'machines_list' and 'machines' arguments isn't allowed")
        module.params["machines"] = module.params["machines_list"]
    module.params.pop("machines_list")

    if module.params["users_list"] is not None:
        if module.params["users"] is not None:
            raise AssertionError("The use of both 'users_list' and 'users' arguments isn't allowed")
        module.params["users"] = module.params["users_list"]
    module.params.pop("users_list")

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
