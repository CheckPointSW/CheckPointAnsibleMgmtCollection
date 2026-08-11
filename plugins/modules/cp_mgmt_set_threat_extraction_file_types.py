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
module: cp_mgmt_set_threat_extraction_file_types
short_description: Edit support settings for multiple Threat Extraction file types in a single request.
description:
  - Edit support settings for multiple Threat Extraction file types in a single request.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  file_types:
    description:
      - List of Threat Extraction file type updates. Each entry sets 'enabled' on the file type identified by 'file-type-id' or 'file-type'.
    type: list
    elements: dict
    suboptions:
      file_type_id:
        description:
          - File type id.
        type: str
      file_type:
        description:
          - File type extension.
        type: str
      enabled:
        description:
          - Enable support for Threat Extraction.
        type: bool
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  domains_to_process:
    description:
      - Indicates which domains to process the commands on. It cannot be used with the details-level full, must be run from the System Domain only and
        with ignore-warnings true. Valid values are, CURRENT_DOMAIN, ALL_DOMAINS_ON_THIS_SERVER.
    type: list
    elements: str
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
- name: set-threat-extraction-file-types
  cp_mgmt_set_threat_extraction_file_types:
    file_types:
    - enabled: false
      file_type: pdf
    - enabled: true
      file_type: docx
    - enabled: true
      file_type_id: 5b8e4a0e-9876-4cba-8aa9-0b1c2d3e4f56
"""

RETURN = """
cp_mgmt_set_threat_extraction_file_types:
  description: The checkpoint set-threat-extraction-file-types output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        file_types=dict(type='list', elements='dict', options=dict(
            file_type_id=dict(type='str'),
            file_type=dict(type='str'),
            enabled=dict(type='bool')
        )),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        domains_to_process=dict(type='list', elements='str'),
        ignore_warnings=dict(type='bool'),
        ignore_errors=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "set-threat-extraction-file-types"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
