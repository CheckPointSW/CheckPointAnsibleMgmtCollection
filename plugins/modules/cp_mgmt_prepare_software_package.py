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
module: cp_mgmt_prepare_software_package
short_description: Prepares the software package on target machines.
description:
  - Prepares the software package on target machines.
  - All operations are performed over Web Services API.
  - Available from R82.20 management version.
version_added: "7.0.0"
author: "Dor Berenstein (@chkp-dorbe)"
options:
  name:
    description:
      - The name of the software package.
    type: str
    required: True
  targets:
    description:
      - On what targets to execute this command. Targets may be identified by their name, or object unique identifier.
    type: list
    elements: str
    required: True
  cluster_installation_settings:
    description:
      - Preparation settings for cluster.
    type: dict
    suboptions:
      cluster_delay:
        description:
          - The delay between end of installation on one cluster members and start of installation on the next cluster member.
        type: int
      cluster_strategy:
        description:
          - The cluster installation strategy.
            all-members - Install the package on all members in the cluster
            non-active-members-and-failover - In the High Availability cluster, install the package only on the selected cluster members with the cluster state
            'Standby' and then failover from the current 'Active' member to one of the updated members
            non-active-members-no-failover - In the High Availability cluster, install the package only on the selected cluster members with the cluster state
            'Standby' and then do not failover from the current 'Active' member to one of the updated members.
        type: str
        choices: ['all-members', 'non-active-members-and-failover', 'non-active-members-no-failover']
  concurrency_limit:
    description:
      - The number of targets, on which the same package is installed at the same time.
    type: int
  package_location:
    description:
      - The package repository.
    type: str
    choices: ['automatic', 'target-machine', 'central']
extends_documentation_fragment: check_point.mgmt.checkpoint_commands
"""

EXAMPLES = """
- name: prepare-software-package
  cp_mgmt_prepare_software_package:
    cluster_installation_settings:
      cluster_strategy: non-active-members-no-failover
    name: Check_Point_R80_40_JHF_MCD_DEMO_019_MAIN_Bundle_T1_VISIBLE_FULL.tgz
    package_location: automatic
    targets:
      - corporate-gateway
"""

RETURN = """
cp_mgmt_prepare_software_package:
  description: The checkpoint prepare-software-package output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        targets=dict(type='list', elements='str', required=True),
        cluster_installation_settings=dict(type='dict', options=dict(
            cluster_delay=dict(type='int'),
            cluster_strategy=dict(type='str', choices=['all-members', 'non-active-members-and-failover', 'non-active-members-no-failover'])
        )),
        concurrency_limit=dict(type='int'),
        package_location=dict(type='str', choices=['automatic', 'target-machine', 'central'])
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "prepare-software-package"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
