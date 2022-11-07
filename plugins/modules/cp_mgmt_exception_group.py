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
module: cp_mgmt_exception_group
short_description: Manages exception-group objects on Check Point over Web Services API
description:
  - Manages exception-group objects on Check Point devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
version_added: "1.0.0"
author: "Or Soffer (@chkp-orso)"
options:
  name:
    description:
      - Object name.
    type: str
    required: True
  applied_profile:
    description:
      - The threat profile to apply this group to in the case of apply-on threat-rules-with-specific-profile.
    type: str
  applied_threat_rules:
    description:
      - The threat rules to apply this group on in the case of apply-on manually-select-threat-rules.
    type: dict
    suboptions:
      add:
        description:
          - Adds to collection of values
        type: list
        elements: dict
        suboptions:
          layer:
            description:
              - The layer of the threat rule to which the group is to be attached.
            type: str
          name:
            description:
              - The name of the threat rule to which the group is to be attached.
            type: str
          rule_number:
            description:
              - The rule-number of the threat rule to which the group is to be attached.
            type: str
          position:
            description:
              - Position in the rulebase.
            type: str
  apply_on:
    description:
      - An exception group can be set to apply on all threat rules, all threat rules which have a specific profile, or those rules manually chosen by the user.
    type: str
    choices: ['all-threat-rules', 'all-threat-rules-with-specific-profile', 'manually-select-threat-rules']
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
- name: add-exception-group
  cp_mgmt_exception_group:
    applied_threat_rules.0.layer: MyLayer
    applied_threat_rules.0.name: MyThreatRule
    apply_on: manually-select-threat-rules
    name: exception_group_2
    state: present

- name: set-exception-group
  cp_mgmt_exception_group:
    apply_on: all-threat-rules
    name: exception_group_2
    state: present
    tags: tag3

- name: delete-exception-group
  cp_mgmt_exception_group:
    name: exception_group_2
    state: absent
"""

RETURN = """
cp_mgmt_exception_group:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import (
    checkpoint_argument_spec_for_objects,
    api_call,
)


def main():
    argument_spec = dict(
        name=dict(type="str", required=True),
        applied_profile=dict(type="str"),
        applied_threat_rules=dict(
            type="dict",
            options=dict(
                add=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        layer=dict(type="str"),
                        name=dict(type="str"),
                        rule_number=dict(type="str"),
                        position=dict(type="str"),
                    ),
                )
            ),
        ),
        apply_on=dict(
            type="str",
            choices=[
                "all-threat-rules",
                "all-threat-rules-with-specific-profile",
                "manually-select-threat-rules",
            ],
        ),
        tags=dict(type="list", elements="str"),
        color=dict(
            type="str",
            choices=[
                "aquamarine",
                "black",
                "blue",
                "crete blue",
                "burlywood",
                "cyan",
                "dark green",
                "khaki",
                "orchid",
                "dark orange",
                "dark sea green",
                "pink",
                "turquoise",
                "dark blue",
                "firebrick",
                "brown",
                "forest green",
                "gold",
                "dark gold",
                "gray",
                "dark gray",
                "light green",
                "lemon chiffon",
                "coral",
                "sea green",
                "sky blue",
                "magenta",
                "purple",
                "slate blue",
                "violet red",
                "navy blue",
                "olive",
                "orange",
                "red",
                "sienna",
                "yellow",
            ],
        ),
        comments=dict(type="str"),
        details_level=dict(type="str", choices=["uid", "standard", "full"]),
        ignore_warnings=dict(type="bool"),
        ignore_errors=dict(type="bool"),
    )
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    api_call_object = "exception-group"

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
