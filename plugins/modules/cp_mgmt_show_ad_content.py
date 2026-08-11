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
module: cp_mgmt_show_ad_content
short_description: Retrieves Active Directory users, groups, and machines for an Account Unit.
description:
  - Retrieves Active Directory users, groups, and machines for an Account Unit.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  account_unit:
    description:
      - Name or UID of the Active Directory Account Unit to query.
    type: str
    required: True
  filter:
    description:
      - Filters the returned entities.
    type: dict
    suboptions:
      text:
        description:
          - Search text. entities matching any of the values are returned.
        type: list
        elements: str
      exact_match:
        description:
          - When true, uses equality match on attributes. When false, uses substring match. Not applicable when 'search-in' is 'anr'.
        type: bool
      search_in:
        description:
          - AD attributes to search in. An entity is returned if text matches in any of the specified attributes. Set to 'anr' to use Ambiguous
            Name Resolution - an AD server-side feature that searches across multiple indexed attributes simultaneously. 'anr' cannot be combined with other
            attributes.
        type: list
        elements: str
      fetch_users:
        description:
          - When true, includes user entities in the results.
        type: bool
      fetch_groups:
        description:
          - When true, includes group entities in the results.
        type: bool
      fetch_machines:
        description:
          - When true, includes machine entities in the results.
        type: bool
  fetch_direct_groups:
    description:
      - When true, returns the direct (first-level) groups each entity belongs to in 'member-of'.
    type: bool
  use_cursor:
    description:
      - When true, enables cursor pagination using LDAP Simple Paged Results. The response carries 'next-cursor', which the caller passes back as
        'cursor' on subsequent requests to fetch the next batch. Cannot be combined with 'offset'. When 'use-cursor' is true, 'total' is not returned in the
        response.
    type: bool
  cursor:
    description:
      - Opaque pagination cursor from a previous response's 'next-cursor'. Omit on the first call of a cursor walk. Requires 'use-cursor' to be true.
    type: str
  limit:
    description:
      - The maximal number of returned results.
    type: int
  offset:
    description:
      - Number of the results to initially skip. Cannot be combined with 'use-cursor' set to true.
    type: int
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: show-ad-content
  cp_mgmt_show_ad_content:
    account_unit: MyActiveDirectory
    limit: 4
"""

RETURN = """
cp_mgmt_show_ad_content:
  description: The checkpoint show-ad-content output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        account_unit=dict(type='str', required=True),
        filter=dict(type='dict', options=dict(
            text=dict(type='list', elements='str'),
            exact_match=dict(type='bool'),
            search_in=dict(type='list', elements='str'),
            fetch_users=dict(type='bool'),
            fetch_groups=dict(type='bool'),
            fetch_machines=dict(type='bool')
        )),
        fetch_direct_groups=dict(type='bool'),
        use_cursor=dict(type='bool'),
        cursor=dict(type='str'),
        limit=dict(type='int'),
        offset=dict(type='int')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "show-ad-content"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
