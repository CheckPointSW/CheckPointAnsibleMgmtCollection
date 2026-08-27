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
module: cp_mgmt_firewall_best_practice
short_description: Manages firewall-best-practice objects on Checkpoint over Web Services API
description:
  - Manages firewall-best-practice objects on Checkpoint devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  name:
    description:
      - Best Practice Name.
    type: str
  action_item:
    description:
      - To comply with Best Practice, do this action item.
    type: str
  description:
    description:
      - Description of the Best Practice.
    type: str
  enabled:
    description:
      - The activation status of the best practice.
    type: bool
  expiration:
    description:
      - Deactivation expiration settings.<br><font color="red">Required only if</font> enabled is set to false.
    type: dict
    suboptions:
      comment:
        description:
          - The reason for deactivating the best practice.
        type: str
      expire_on:
        description:
          - When the deactivation expires. Date and time represented in international ISO 8601 format. Relevant only if mode is set to 'expire-on'.
        type: str
      mode:
        description:
          - Whether the deactivation never expires or expires on a specific date.
        type: str
        choices: ['never', 'expire-on']
  policy_range_percentage:
    description:
      - The percentage of the Rule Base to scan (0-100).
    type: int
  policy_range_position:
    description:
      - The direction of the scan.
    type: str
    choices: ['top', 'bottom']
  poor_condition:
    description:
      - Visibility of poor-result rules in the Relevant Objects pane.
    type: str
    choices: ['display rules that match', "display rules that don't match", "don't display rules"]
  rule:
    description:
      - The rule criteria the firewall best practice evaluates against the rule base. Multi-set semantics on all match-list fields except name and comment.
    type: dict
    suboptions:
      source:
        description:
          - Network objects to match in the rule Source column.
            Identified by name or UID.
        type: list
        elements: str
      negate_source:
        description:
          - Shows if the source values are negated.
        type: bool
      destination:
        description:
          - Network objects to match in the rule Destination column.
            Identified by name or UID.
        type: list
        elements: str
      negate_destination:
        description:
          - Shows if the destination values are negated.
        type: bool
      vpn:
        description:
          - VPN communities to match.
            Identified by name or UID.
        type: list
        elements: str
      negate_vpn:
        description:
          - Shows if the vpn values are negated.
        type: bool
      services_and_applications:
        description:
          - Services, applications, categories or sites to match.
            Identified by name or UID.
        type: list
        elements: str
      negate_services_and_applications:
        description:
          - Shows if the services and applications values are negated.
        type: bool
      install_on:
        description:
          - Security Gateways or Clusters the rule applies to.
            Identified by name or UID.
        type: list
        elements: str
      negate_install_on:
        description:
          - Shows if the install-on values are negated.
        type: bool
      time:
        description:
          - Time objects the rule applies to.
            Identified by name or UID.
        type: list
        elements: str
      negate_time:
        description:
          - Shows if the time values are negated.
        type: bool
      action:
        description:
          - Rule actions to match.
        type: list
        elements: str
      negate_action:
        description:
          - Shows if the action values are negated.
        type: bool
      track:
        description:
          - Tracking methods to match.
        type: list
        elements: str
      negate_track:
        description:
          - Shows if the track values are negated.
        type: bool
      hit_count:
        description:
          - Hit-count levels to match.
        type: list
        elements: str
      negate_hit_count:
        description:
          - Shows if the hit-count values are negated.
        type: bool
      name_condition:
        description:
          - Match the rule name against a text condition.
        type: dict
        suboptions:
          condition_type:
            description:
              - The condition type.
            type: str
            choices: ['any', 'blank', 'not blank', 'starts with', 'equals', 'ends with', 'contains']
          value:
            description:
              - The condition match string. Relevant only when the value of the 'condition-type' parameter is, 'Equals', 'Starts with', 'Ends
                with', 'Contains'.
            type: str
      comment_condition:
        description:
          - Match the rule comment against a text condition.
        type: dict
        suboptions:
          condition_type:
            description:
              - The condition type.
            type: str
            choices: ['any', 'blank', 'not blank', 'starts with', 'equals', 'ends with', 'contains']
          value:
            description:
              - The condition match string. Relevant only when the value of the 'condition-type' parameter is, 'Equals', 'Starts with', 'Ends
                with', 'Contains'.
            type: str
  secure_condition:
    description:
      - Visibility of secure-result rules in the Relevant Objects pane.
    type: str
    choices: ['display rules that match', "display rules that don't match", "don't display rules"]
  tolerance:
    description:
      - Number of matches allowed before a violation is created. Valid values, between 0 and 100.<br><font color="red">Required only if</font>
        violation-condition is set to 'Rule found'.
    type: int
  violation_condition:
    description:
      - Define when a violation occurs, 'Rule found' means the criteria match a rule; 'Rule not found' means no rule matches.
    type: str
    choices: ['rule found', 'rule not found']
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
  best_practice_id:
    description:
      - Best Practice ID.
    type: str
extends_documentation_fragment: check_point.mgmt.checkpoint_objects
"""

EXAMPLES = """
- name: add-firewall-best-practice
  cp_mgmt_firewall_best_practice:
    action_item: Define a clean-up rule at the end of the policy.
    description: Checks that the rule base ends with a clean-up rule.
    enabled: true
    name: Clean-up rule defined in Access Policy
    rule:
      action:
        - drop
      destination:
        - Any
      hit_count:
        - low
      name_condition:
        condition_type: contains
        value: cleanup
      source:
        - Any
      track:
        - log
    state: present

- name: set-firewall-best-practice
  cp_mgmt_firewall_best_practice:
    best_practice_id: FW001
    enabled: false
    expiration:
      comment: Temporarily disabled pending policy review.
      expire_on: '2026-12-31T14:30:00'
      mode: expire-on
    state: present

- name: delete-firewall-best-practice
  cp_mgmt_firewall_best_practice:
    best_practice_id: FW001
    state: absent
"""

RETURN = """
cp_mgmt_firewall_best_practice:
  description: The checkpoint object created or updated.
  returned: always, except when deleting the object.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_objects, api_call


def main():
    argument_spec = dict(
        name=dict(type='str'),
        action_item=dict(type='str'),
        description=dict(type='str'),
        enabled=dict(type='bool'),
        expiration=dict(type='dict', options=dict(
            comment=dict(type='str'),
            expire_on=dict(type='str'),
            mode=dict(type='str', choices=['never', 'expire-on'])
        )),
        policy_range_percentage=dict(type='int'),
        policy_range_position=dict(type='str', choices=['top', 'bottom']),
        poor_condition=dict(type='str', choices=['display rules that match', "display rules that don't match", "don't display rules"]),
        rule=dict(type='dict', options=dict(
            source=dict(type='list', elements='str'),
            negate_source=dict(type='bool'),
            destination=dict(type='list', elements='str'),
            negate_destination=dict(type='bool'),
            vpn=dict(type='list', elements='str'),
            negate_vpn=dict(type='bool'),
            services_and_applications=dict(type='list', elements='str'),
            negate_services_and_applications=dict(type='bool'),
            install_on=dict(type='list', elements='str'),
            negate_install_on=dict(type='bool'),
            time=dict(type='list', elements='str'),
            negate_time=dict(type='bool'),
            action=dict(type='list', elements='str'),
            negate_action=dict(type='bool'),
            track=dict(type='list', elements='str'),
            negate_track=dict(type='bool'),
            hit_count=dict(type='list', elements='str'),
            negate_hit_count=dict(type='bool'),
            name_condition=dict(type='dict', options=dict(
                condition_type=dict(type='str', choices=['any', 'blank', 'not blank', 'starts with', 'equals', 'ends with', 'contains']),
                value=dict(type='str')
            )),
            comment_condition=dict(type='dict', options=dict(
                condition_type=dict(type='str', choices=['any', 'blank', 'not blank', 'starts with', 'equals', 'ends with', 'contains']),
                value=dict(type='str')
            ))
        )),
        secure_condition=dict(type='str', choices=['display rules that match', "display rules that don't match", "don't display rules"]),
        tolerance=dict(type='int'),
        violation_condition=dict(type='str', choices=['rule found', 'rule not found']),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool'),
        best_practice_id=dict(type='str')
    )
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    api_call_object = 'firewall-best-practice'

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
