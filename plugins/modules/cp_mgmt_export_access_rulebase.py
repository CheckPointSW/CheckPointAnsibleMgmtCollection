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
module: cp_mgmt_export_access_rulebase
short_description: Retrieve the entire content of an Access Rules layer.
description:
  - Retrieve the entire content of an Access Rules layer. The reply features a list of objects; Each object in the reply may be a section of the layer,
    with all its rules in, or a rule itself, for the case of rules which are under the global section. In case a rule has an Access Layer applied on it, the
    entire content of the inline layer will be included in the reply as well.
  - All operations are performed over Web Services API.
  - Available from R82.20 Management version.
version_added: "6.9.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  name:
    description:
      - Object name. Must be unique in the domain.
    type: str
  package:
    description:
      - Name of the package.
    type: str
  show_expiration_settings:
    description:
      - Indicates whether to calculate and show "expiration date settings" field in reply.
    type: bool
  show_hits:
    description:
      - Show hitcount data.
    type: bool
  use_object_dictionary:
    description:
      - N/A
    type: bool
  hits_settings:
    description:
      - Hitcount settings, define the range if hits to show.
    type: dict
    suboptions:
      from_date:
        description:
          - Format, YYYY-MM-DD, YYYY-mm-ddThh,mm,ss.
        type: str
      target:
        description:
          - Target gateway name or UID.
        type: str
      to_date:
        description:
          - Format, YYYY-MM-DD, YYYY-mm-ddThh,mm,ss.
        type: str
  dereference_group_members:
    description:
      - Indicates whether to dereference "members" field by details level for every object in reply.
    type: bool
  show_membership:
    description:
      - Indicates whether to calculate and show "groups" field for every object in reply.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: export-access-rulebase
  cp_mgmt_export_access_rulebase:
    name: Corp-Access
"""

RETURN = """
cp_mgmt_export_access_rulebase:
  description: The checkpoint export-access-rulebase output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        name=dict(type='str'),
        package=dict(type='str'),
        show_expiration_settings=dict(type='bool'),
        show_hits=dict(type='bool'),
        use_object_dictionary=dict(type='bool'),
        hits_settings=dict(type='dict', options=dict(
            from_date=dict(type='str'),
            target=dict(type='str'),
            to_date=dict(type='str')
        )),
        dereference_group_members=dict(type='bool'),
        show_membership=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "export-access-rulebase"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
