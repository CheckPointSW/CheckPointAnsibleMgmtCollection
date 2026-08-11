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
module: cp_mgmt_test_ai_agent_security_api_key
short_description: Test the validity of an AI Agent Security API key.
description:
  - Test the validity of an AI Agent Security API key. Optionally validates that a project ID belongs to the key. The management server sends a test
    request to AI Agent Security and returns whether the key (and project) is valid.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  project_id:
    description:
      - Optional AI Agent Security project ID to validate. If provided, also verifies the project belongs to the API key.
    type: str
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: test-ai-agent-security-api-key
  cp_mgmt_test_ai_agent_security_api_key:
    project_id: 550e8400-e29b-41d4-a716-446655440000
"""

RETURN = """
cp_mgmt_test_ai_agent_security_api_key:
  description: The checkpoint test-ai-agent-security-api-key output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        project_id=dict(type='str')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "test-ai-agent-security-api-key"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
