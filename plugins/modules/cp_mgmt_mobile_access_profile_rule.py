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
module: cp_mgmt_mobile_access_profile_rule
short_description: Manages mobile-access-profile-rule objects on Checkpoint over Web Services API
description:
  - Manages mobile-access-profile-rule objects on Checkpoint devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
version_added: "6.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  position:
    description:
      - Position in the rulebase.
    type: str
  name:
    description:
      - Object name.
    type: str
    required: True
  mobile_profile:
    description:
      - Profile configuration for User groups - identified by the name or UID.
    type: str
  user_groups:
    description:
      - User groups that will be configured with the profile object - identified by the name or UID.
    type: list
    elements: str
  enabled:
    description:
      - Enable/Disable the rule.
    type: bool
  tags:
    description:
      - Collection of tag identifiers.
    type: list
    elements: str
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
- name: add-mobile-access-profile-rule
  cp_mgmt_mobile_access_profile_rule:
    mobile_profile: Default_Profile
    name: Rule 1
    position: 1
    state: present
    user_groups:
    - my_group

- name: set-mobile-access-profile-rule
  cp_mgmt_mobile_access_profile_rule:
    mobile_profile: Default_Profile
    name: Rule 1
    position: 2
    user_groups:
    - my_group
    state: present

- name: delete-mobile-access-profile-rule
  cp_mgmt_mobile_access_profile_rule:
    name: New Mobile Profile Rule
    state: absent
"""

RETURN = """
cp_mgmt_mobile_access_profile_rule:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_objects, api_call, api_call_for_rule


def main():
    argument_spec = dict(
        position=dict(type='str'),
        name=dict(type='str', required=True),
        mobile_profile=dict(type='str'),
        user_groups=dict(type='list', elements='str'),
        enabled=dict(type='bool'),
        tags=dict(type='list', elements='str'),
        comments=dict(type='str'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    api_call_object = 'mobile-access-profile-rule'

    if module.params["position"] is None:
        result = api_call(module, api_call_object)
    else:
        result = api_call_for_rule(module, api_call_object)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
