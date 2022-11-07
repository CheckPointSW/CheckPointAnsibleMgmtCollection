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
module: cp_mgmt_reset_sic
short_description: Reset Secure Internal Communication (SIC). To complete the reset operation need also to reset the device in the Check Point Configuration
                   Tool (by running cpconfig in Clish or Expert mode). Communication will not be possible until you reset and re-initialize the device properly.
description:
  - Reset Secure Internal Communication (SIC). To complete the reset operation need also to reset the device in the Check Point Configuration Tool (by
    running cpconfig in Clish or Expert mode). Communication will not be possible until you reset and re-initialize the device properly.
  - All operations are performed over Web Services API.
version_added: "3.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  name:
    description:
      - Gateway, cluster member or Check Point host name.
    type: str
  auto_publish_session:
    description:
    - Publish the current session if changes have been performed after task completes.
    type: bool
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: reset-sic
  cp_mgmt_reset_sic:
    name: gw1
"""

RETURN = """
cp_mgmt_reset_sic:
  description: The checkpoint reset-sic output.
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
        name=dict(type="str"), auto_publish_session=dict(type="bool")
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "reset-sic"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
