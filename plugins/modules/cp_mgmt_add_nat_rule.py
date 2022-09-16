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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: cp_mgmt_add_nat_rule
short_description: Create new object.
description:
  - Create new object.
  - All operations are performed over Web Services API.
version_added: "2.0.0"
author: "Or Soffer (@chkp-orso)"
options:
  package:
    description:
      - Name of the package.
    type: str
  position:
    description:
      - Position in the rulebase.
    type: str
  enabled:
    description:
      - Enable/Disable the rule.
    type: bool
  install_on:
    description:
      - Which Gateways identified by the name or UID to install the policy on.
    type: list
    elements: str
  method:
    description:
      - Nat method.
    type: str
    choices: ['static', 'hide', 'nat64', 'nat46']
  original_destination:
    description:
      - Original destination.
    type: str
  original_service:
    description:
      - Original service.
    type: str
  original_source:
    description:
      - Original source.
    type: str
  translated_destination:
    description:
      - Translated  destination.
    type: str
  translated_service:
    description:
      - Translated  service.
    type: str
  translated_source:
    description:
      - Translated  source.
    type: str
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
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: add-nat-rule
  cp_mgmt_add_nat_rule:
    comments: comment example1 nat999
    enabled: false
    install_on:
    - Policy Targets
    original_destination: All_Internet
    original_source: Any
    package: standard
    position: 1
    state: present
"""

RETURN = """
cp_mgmt_add_nat_rule:
  description: The checkpoint add-nat-rule output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import (
    checkpoint_argument_spec_for_commands,
    api_command,
)


def main():
    argument_spec = dict(
        package=dict(type="str"),
        position=dict(type="str"),
        enabled=dict(type="bool"),
        install_on=dict(type="list", elements="str"),
        method=dict(type="str", choices=["static", "hide", "nat64", "nat46"]),
        original_destination=dict(type="str"),
        original_service=dict(type="str"),
        original_source=dict(type="str"),
        translated_destination=dict(type="str"),
        translated_service=dict(type="str"),
        translated_source=dict(type="str"),
        comments=dict(type="str"),
        details_level=dict(type="str", choices=["uid", "standard", "full"]),
        ignore_warnings=dict(type="bool"),
        ignore_errors=dict(type="bool"),
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "add-nat-rule"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
