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
module: cp_mgmt_set_app_control_update_schedule
short_description: Set the Application Control and URL Filtering update schedule.
description:
  - Set the Application Control and URL Filtering update schedule.
  - All operations are performed over Web Services API.
  - Available from R82 JHF management version.
version_added: "6.5.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  schedule_management_update:
    description:
      - Application Control & URL Filtering Update Schedule on Management Server.
    type: dict
    suboptions:
      enabled:
        description:
          - Enable/Disable Application Control & URL Filtering Update Schedule on Management Server.
        type: bool
      schedule:
        description:
          - Schedule Configuration.
        type: dict
        suboptions:
          time:
            description:
              - Time in format HH,mm.
            type: str
          recurrence:
            description:
              - Days recurrence.
            type: dict
            suboptions:
              pattern:
                description:
                  - Days recurrence pattern.
                type: str
                choices: ['Daily', 'Weekly', 'Monthly']
              weekdays:
                description:
                  - Days of the week to run the update.<br> Valid values, group of values from {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri',
                    'Sat'}. <font color="red">Required only when</font> pattern is set to 'Weekly'.
                type: list
                elements: str
              days:
                description:
                  - Days of the month to run the update.<br> Valid values, interval in the range of 1 to 31. <font color="red">Required
                    only when</font> pattern is set to 'Monthly'.
                type: list
                elements: str
  schedule_gateway_update:
    description:
      - Application Control & URL Filtering Update Schedule on Gateway.
    type: dict
    suboptions:
      enabled:
        description:
          - Enable/Disable Application Control & URL Filtering Update Schedule on Gateway.
        type: bool
      schedule:
        description:
          - Schedule Configuration.
        type: dict
        suboptions:
          time:
            description:
              - Time in format HH,mm.
            type: str
          recurrence:
            description:
              - Days recurrence.
            type: dict
            suboptions:
              pattern:
                description:
                  - Days recurrence pattern.
                type: str
                choices: ['Daily', 'Weekly', 'Monthly', 'Interval']
              interval_hours:
                description:
                  - The amount of hours between updates. <font color="red">Required only when</font> pattern is set to 'Interval'.
                type: int
              interval_minutes:
                description:
                  - The amount of minutes between updates. <font color="red">Required only when</font> pattern is set to 'Interval'.
                type: int
              interval_seconds:
                description:
                  - The amount of seconds between updates. <font color="red">Required only when</font> pattern is set to 'Interval'.
                type: int
              weekdays:
                description:
                  - Days of the week to run the update.<br> Valid values, group of values from {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri',
                    'Sat'}. <font color="red">Required only when</font> pattern is set to 'Weekly'.
                type: list
                elements: str
              days:
                description:
                  - Days of the month to run the update.<br> Valid values, interval in the range of 1 to 31. <font color="red">Required
                    only when</font> pattern is set to 'Monthly'.
                type: list
                elements: str
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: set-app-control-update-schedule
  cp_mgmt_set_app_control_update_schedule:
    schedule_gateway_update:
      schedule:
        recurrence:
          interval_hours: 4
          interval_minutes: 30
          interval_seconds: 10
          pattern: interval
    state: present
"""

RETURN = """
cp_mgmt_set_app_control_update_schedule:
  description: The checkpoint set-app-control-update-schedule output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        schedule_management_update=dict(type='dict', options=dict(
            enabled=dict(type='bool'),
            schedule=dict(type='dict', options=dict(
                time=dict(type='str'),
                recurrence=dict(type='dict', options=dict(
                    pattern=dict(type='str', choices=['Daily', 'Weekly', 'Monthly']),
                    weekdays=dict(type='list', elements="str"),
                    days=dict(type='list', elements="str")
                ))
            ))
        )),
        schedule_gateway_update=dict(type='dict', options=dict(
            enabled=dict(type='bool'),
            schedule=dict(type='dict', options=dict(
                time=dict(type='str'),
                recurrence=dict(type='dict', options=dict(
                    pattern=dict(type='str', choices=['Daily', 'Weekly', 'Monthly', 'Interval']),
                    interval_hours=dict(type='int'),
                    interval_minutes=dict(type='int'),
                    interval_seconds=dict(type='int'),
                    weekdays=dict(type='list', elements="str"),
                    days=dict(type='list', elements="str")
                ))
            ))
        ))
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "set-app-control-update-schedule"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
