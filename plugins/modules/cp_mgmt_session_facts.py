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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: cp_mgmt_session_facts
short_description: Get session objects facts on Check Point over Web Services API
description:
  - Get session objects facts on Check Point devices.
  - All operations are performed over Web Services API.
  - This module handles both operations, get a specific object and get several objects,
    For getting a specific object use the parameter 'name'.
version_added: "1.0.0"
author: "Or Soffer (@chkp-orso)"
options:
  limit:
    description:
      - No more than that many results will be returned.
        This parameter is relevant only for getting few objects.
    type: int
  offset:
    description:
      - Skip that many results before beginning to return them.
        This parameter is relevant only for getting few objects.
    type: int
  order:
    description:
      - Sorts results by the given field. By default the results are sorted in the descending order by the session publish time.
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
  view_published_sessions:
    description:
      - Show a list of published sessions.
    type: bool
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
extends_documentation_fragment: check_point.mgmt.checkpoint_facts
"""

EXAMPLES = """
- name: show-session
  cp_mgmt_session_facts:

- name: show-sessions
  cp_mgmt_session_facts:
    details_level: standard
    limit: 50
    offset: 0
"""

RETURN = """
ansible_facts:
  description: The checkpoint object facts.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import (
    checkpoint_argument_spec_for_facts,
    api_call_facts,
)


def main():
    argument_spec = dict(
        limit=dict(type="int"),
        offset=dict(type="int"),
        order=dict(
            type="list",
            elements="dict",
            options=dict(
                ASC=dict(type="str", choices=["name"]),
                DESC=dict(type="str", choices=["name"]),
            ),
        ),
        view_published_sessions=dict(type="bool"),
        details_level=dict(type="str", choices=["uid", "standard", "full"]),
    )
    argument_spec.update(checkpoint_argument_spec_for_facts)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )

    api_call_object = "session"
    api_call_object_plural_version = "sessions"

    result = api_call_facts(
        module, api_call_object, api_call_object_plural_version
    )
    module.exit_json(ansible_facts=result)


if __name__ == "__main__":
    main()
