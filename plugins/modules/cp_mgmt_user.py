#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
---
module: cp_mgmt_user
short_description: Manages user objects on Checkpoint over Web Services API
description:
  - Manages user objects on Checkpoint devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
version_added: "xxx"
author: "Christoph Spatt (@edeka-spatt)"
options:
  name:
    description:
      - Object name.
    type: str
    required: True
  email:
    description:
      - Email Address.
    type: str
  expiration_date:
    description:
      - User expiration date in format: yyyy-MM-dd.
    type: str
  phone_number:
    description:
      - Phone number.
    type: str
  authentication_method:
    description:
      - Authentication method.
    type: str
    choices: ['undefined', 'check point password', 'os password', 'securid', 'radius', 'tacacs']
  password:
    description:
      - User password.
    type: str
  radius_server:
    description:
      - RADIUS server object identified by the name or UID. Must be set when "authentication-method" was selected to be "RADIUS".
    type: str
  tacacs_server:
    description:
      - TACACS server object identified by the name or UID. Must be set when "authentication-method" was selected to be "TACACS".
    type: str
  connect_on_days:
    description:
      - Days users allow to connect. Mutual exclusive with connect_on_days.
    type: str
  connect_daily:
    description:
      - Connect every day. Mutual exclusive with connect_daily.
    type: bool
  from_hour:
    description:
      - Allow users connect from hour. Format: HH:MM
    type: str
  to_hour:
    description:
      - Allow users connect until hour. Format: HH:MM
    type: str
  allowed_locations:
    description:
      - User allowed locations.
    type: dict
    elements: list
  certificates:
    description:
      - User certificates.
    type: dict
    elements: list
  encryption:
    description:
      - User encryption.
    type: dict
    elements: str
  groups:
    description:
      - Collection of group identifiers.
    type: list
    elements: str
  tags:
    description:
      - Collection of tag identifiers.
    type: list
    elements: str
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
- name: add-user
  cp_mgmt_user:
    name: myuser
    email: myuser@email.com
    groups:
    - myusergroup
    authentication_method: check point password
    password: mypass
    state: present

- name: set-user
  cp_mgmt_user:
    email: myuser123@email.com
    name: myuser
    state: present

- name: delete-user
  cp_mgmt_user:
    name: myuser
    state: absent
"""

RETURN = """
cp_mgmt_user:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_objects, api_call


def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        email=dict(type='str'),
        expiration_date=dict(type='str'),
        phone_number=dict(type='str'),
        authentication_method=dict(type='str', choices=['undefined', 'check point password', 'os password', 'securid', 'radius', 'tacacs']),
        password=dict(type='str', no_log=True),
        radius_server=dict(type='str'),
        tacacs_server=dict(type='str'),
        connect_on_days=dict(type='str'),
        connect_daily=dict(type='bool'),
        from_hour=dict(type='str'),
        to_hour=dict(type='str'),
        allowed_locations=dict(
            type="dict",
            elements="dict",
            options=dict(destinations=dict(type="list"), sources=dict(type="list")),
        ),
        certificates=dict(
            type="dict",
            elements="dict",
            options=dict(add=dict(type="list"), remove=dict(type="list")),
        ),
        encryption=dict(
            type="dict",
            elements="str"
        ),
        groups=dict(type='list', elements='str'),
        tags=dict(type='list', elements='str'),
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
    api_call_object = 'user'

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
