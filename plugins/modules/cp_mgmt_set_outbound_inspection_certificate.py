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
module: cp_mgmt_set_outbound_inspection_certificate
short_description: Create or update a certificate to be used as outbound certificate for HTTPS inspection.
                   <br>The outbound CA certificate will be used by the Gateway to inspect SSL traffic.
description:
  - Create or update a certificate to be used as outbound certificate for HTTPS inspection. <br>The outbound CA certificate will be used by the Gateway to
    inspect SSL traffic.
  - All operations are performed over Web Services API.
version_added: "3.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  issued_by:
    description:
      - The DN (Distinguished Name) of the certificate.
    type: str
  base64_password:
    description:
      - Password (encoded in Base64 with padding) for the certificate file.
    type: str
  valid_from:
    description:
      - The date, from which the certificate is valid. Format, YYYY-MM-DD.
    type: str
  valid_to:
    description:
      - The certificate expiration date. Format, YYYY-MM-DD.
    type: str
  details_level:
    description:
      - The level of detail for some of the fields in the response can vary from showing only the UID value of the object to a fully detailed
        representation of the object.
    type: str
    choices: ['uid', 'standard', 'full']
  auto_publish_session:
    description:
    - Publish the current session if changes have been performed after task completes.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: set-outbound-inspection-certificate
  cp_mgmt_set_outbound_inspection_certificate:
    base64_password: bXlfcGFzc3dvcmQ=
    issued_by: www.checkpoint.com
    state: present
    valid_from: '2021-04-17'
    valid_to: '2028-04-17'
"""

RETURN = """
cp_mgmt_set_outbound_inspection_certificate:
  description: The checkpoint set-outbound-inspection-certificate output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        issued_by=dict(type='str'),
        base64_password=dict(type='str', no_log=True),
        valid_from=dict(type='str'),
        valid_to=dict(type='str'),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        auto_publish_session=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "set-outbound-inspection-certificate"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
