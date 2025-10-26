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
module: cp_mgmt_vpn_community_star
short_description: Manages vpn-community-star objects on Check Point over Web Services API
description:
  - Manages vpn-community-star objects on Check Point devices including creating, updating and removing objects.
  - All operations are performed over Web Services API.
  - Available from R80 management version.
version_added: "1.0.0"
author: "Or Soffer (@chkp-orso)"
options:
  name:
    description:
      - Object name.
    type: str
    required: True
  center_gateways:
    description:
      - Collection of center VPN Gateway and VPN Device objects identified by the name or UID.
    type: list
    elements: str
  disable_nat:
    description:
      - Indicates whether to disable NAT inside the VPN Community.
      - Available from R82 JHF management version.
    type: bool
    version_added: "6.5.0"
  disable_nat_on:
    description:
      - Indicates on which gateways to disable NAT inside the VPN Community.
      - Available from R82 JHF management version.
    type: str
    choices: ['satellite gateways only', 'both center and satellite gateways']
    version_added: "6.5.0"
  encrypted_traffic:
    description:
      - Encrypted traffic settings.
      - Available from R82 JHF management version.
    type: dict
    version_added: "6.5.0"
    suboptions:
      enabled:
        description:
          - Indicates whether to accept all encrypted traffic.
        type: bool
      community_members:
        description:
          - Indicates on which community members to accept all encrypted traffic.
        type: str
        choices: ['satellite gateways only', 'both center and satellite gateways']
  encryption_method:
    description:
      - The encryption method to be used.
      - Available from R80.10 management version.
    type: str
    choices: ['prefer ikev2 but support ikev1', 'ikev2 only', 'ikev1 for ipv4 and ikev2 for ipv6 only']
  encryption_suite:
    description:
      - The encryption suite to be used.
      - Available from R80.10 management version.
    type: str
    choices: ['suite-b-gcm-256', 'custom', 'vpn b', 'vpn a', 'suite-b-gcm-128']
  excluded_services:
    description:
      - Collection of services that are excluded from the community identified by the name or UID.<br> Connections with these services will not be
        encrypted and will not match rules specifying the community in the VPN community.
      - Available from R82 JHF management version.
    type: list
    elements: str
    version_added: "6.5.0"
  granular_encryptions:
    description:
      - VPN granular encryption settings.
      - Available from R81 management version.
    type: list
    elements: dict
    version_added: "5.1.0"
    suboptions:
      internal_gateway:
        description:
          - Internally managed Check Point gateway identified by name or UID, or 'Any' for all internal-gateways participants in this community.
        type: str
      external_gateway:
        description:
          - Externally managed or 3rd party gateway identified by name or UID.
        type: str
      encryption_method:
        description:
          - The encryption method to be used.
        type: str
        choices: ['prefer ikev2 but support ikev1', 'ikev2 only', 'ikev1 for ipv4 and ikev2 for ipv6 only']
      encryption_suite:
        description:
          - The encryption suite to be used.
        type: str
        choices: ['suite-b-gcm-256', 'custom', 'vpn b', 'vpn a', 'suite-b-gcm-128']
      ike_phase_1:
        description:
          - Ike Phase 1 settings. Only applicable when the encryption-suite is set to [custom].
        type: dict
        suboptions:
          encryption_algorithm:
            description:
              - The encryption algorithm to be used.
            type: str
            choices: ['cast', 'aes-256', 'des', 'aes-128', '3des']
          data_integrity:
            description:
              - The hash algorithm to be used.
            type: str
            choices: ['aes-xcbc', 'sha1', 'sha256', 'sha384', 'sha512', 'md5']
          diffie_hellman_group:
            description:
              - The Diffie-Hellman group to be used.
            type: str
            choices: ['group-1', 'group-2', 'group-5', 'group-14', 'group-15', 'group-16', 'group-17', 'group-18', 'group-19', 'group-20', 'group-24']
          ike_p1_rekey_time:
            description:
              - Indicates the time interval for IKE phase 1 renegotiation.
              - Available from R81 management version.
            type: int
          ike_p1_rekey_time_unit:
            description:
              - Indicates the time unit for [ike-p1-rekey-time-unit] parameter, rounded up to minutes scale.
              - Available from R81 management version.
            type: str
            choices: ['days', 'hours', 'minutes', 'seconds']
      ike_phase_2:
        description:
          - Ike Phase 2 settings. Only applicable when the encryption-suite is set to [custom].
        type: dict
        suboptions:
          encryption_algorithm:
            description:
              - The encryption algorithm to be used.
            type: str
            choices: ['cast', 'aes-gcm-256', 'cast-40', 'aes-256', 'des', 'aes-128', '3des', 'des-40cp', 'aes-gcm-128', 'none']
          data_integrity:
            description:
              - The hash algorithm to be used.
            type: str
            choices: ['aes-xcbc', 'sha1', 'sha256', 'sha384', 'sha512', 'md5']
          ike_p2_use_pfs:
            description:
              - Indicates whether Perfect Forward Secrecy (PFS) is being used for IKE phase 2.
            type: bool
          ike_p2_pfs_dh_grp:
            description:
              - The Diffie-Hellman group to be used.
            type: str
            choices: ['group-1', 'group-2', 'group-5', 'group-14', 'group-15', 'group-16', 'group-17', 'group-18', 'group-19', 'group-20', 'group-24']
          ike_p2_rekey_time:
            description:
              - Indicates the time interval for IKE phase 2 renegotiation.
              - Available from R81 management version.
            type: int
          ike_p2_rekey_time_unit:
            description:
              - Indicates the time unit for [ike-p2-rekey-time-unit] parameter.
              - Available from R81 management version.
            type: str
            choices: ['days', 'hours', 'minutes', 'seconds']
  ike_phase_1:
    description:
      - Ike Phase 1 settings. Only applicable when the encryption-suite is set to [custom].
      - Available from R80.10 management version.
    type: dict
    suboptions:
      data_integrity:
        description:
          - The hash algorithm to be used.
        type: str
        choices: ['aes-xcbc', 'sha1', 'sha256', 'sha384', 'sha512', 'md5']
      diffie_hellman_group:
        description:
          - The Diffie-Hellman group to be used.
        type: str
        choices: ['group-1', 'group-2', 'group-5', 'group-14', 'group-19', 'group-20']
      encryption_algorithm:
        description:
          - The encryption algorithm to be used.
        type: str
        choices: ['cast', 'aes-256', 'des', 'aes-128', '3des']
      ike_p1_rekey_time:
        description:
          - Indicates the time interval for IKE phase 1 renegotiation.
          - Available from R81 management version.
        type: int
        version_added: "5.1.0"
      ike_p1_rekey_time_unit:
        description:
          - Indicates the time unit for [ike-p1-rekey-time-unit] parameter, rounded up to minutes scale.
          - Available from R81 management version.
        type: str
        choices: ['days', 'hours', 'minutes', 'seconds']
        version_added: "5.1.0"
  ike_phase_2:
    description:
      - Ike Phase 2 settings. Only applicable when the encryption-suite is set to [custom].
      - Available from R80.10 management version.
    type: dict
    suboptions:
      data_integrity:
        description:
          - The hash algorithm to be used.
        type: str
        choices: ['aes-xcbc', 'sha1', 'sha256', 'sha384', 'sha512', 'md5']
      encryption_algorithm:
        description:
          - The encryption algorithm to be used.
        type: str
        choices: ['cast', 'aes-gcm-256', 'cast-40', 'aes-256', 'des', 'aes-128', '3des', 'des-40cp', 'aes-gcm-128', 'none']
      ike_p2_use_pfs:
        description:
          - Indicates whether Perfect Forward Secrecy (PFS) is being used for IKE phase 2.
          - Available from R81 management version.
        type: bool
        version_added: "5.1.0"
      ike_p2_pfs_dh_grp:
        description:
          - The Diffie-Hellman group to be used.
        type: str
        choices: ['group-1', 'group-2', 'group-5', 'group-14', 'group-15', 'group-16', 'group-17', 'group-18', 'group-19', 'group-20', 'group-24']
        version_added: "5.1.0"
      ike_p2_rekey_time:
        description:
          - Indicates the time interval for IKE phase 2 renegotiation.
          - Available from R81 management version.
        type: int
        version_added: "5.1.0"
      ike_p2_rekey_time_unit:
        description:
          - Indicates the time unit for [ike-p2-rekey-time-unit] parameter.
          - Available from R81 management version.
        type: str
        choices: ['days', 'hours', 'minutes', 'seconds']
        version_added: "5.1.0"
  mep:
    description:
      - Multiple Entry Point properties.
      - Available from R82 JHF management version.
    type: dict
    version_added: "6.5.0"
    suboptions:
      enabled:
        description:
          - Enable center gateways as Multiple Entry Points.
        type: bool
      entry_point_selection_mechanism:
        description:
          - The method by which the entry point gateway will be chosen from the gateways in the center.
        type: str
        choices: ['closest gateway to source', 'closest gateway to destination', 'random selection', 'manual']
      entry_point_final_selection_mechanism:
        description:
          - The method by which the final entry point gateway will be chosen when the chosen mechanism returns more than one optional entry point.
        type: str
        choices: ['random selection', 'first to respond']
      tracking:
        description:
          - Tracking option for the MEP.
        type: str
        choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                 'user defined alert no.3']
      default_priority_rule:
        description:
          - Priority rule for all satellite gateways. Relevant only if 'entry-point-selection-mechanism' is set to 'manual'.
        type: dict
        suboptions:
          first_priority_center_gateways:
            description:
              - Collection of first priority center gateways identified by the name or UID.
            type: list
            elements: str
          second_priority_center_gateways:
            description:
              - Collection of second priority center gateways identified by the name or UID.
            type: list
            elements: str
          third_priority_center_gateways:
            description:
              - Collection of third priority center gateways identified by the name or UID.
            type: list
            elements: str
      exception_priority_rules:
        description:
          - Exception priority rules for specific satellites gateways. Relevant only if 'entry-point-selection-mechanism' is set to 'manual'.
        type: list
        elements: dict
        suboptions:
          satellite_gateways:
            description:
              - Collection of satellite gateways to apply priority rules on identified by the name or UID.
            type: list
            elements: str
          first_priority_center_gateways:
            description:
              - Collection of first priority center gateways identified by the name or UID.
            type: list
            elements: str
          second_priority_center_gateways:
            description:
              - Collection of second priority center gateways identified by the name or UID.
            type: list
            elements: str
          third_priority_center_gateways:
            description:
              - Collection of third priority center gateways identified by the name or UID.
            type: list
            elements: str
  mesh_center_gateways:
    description:
      - Indicates whether the meshed community is in center.
    type: bool
  override_vpn_domains:
    description:
      - The Overrides VPN Domains of the participants GWs.
      - Available from R80.40 management version.
    type: list
    elements: dict
    version_added: "5.1.0"
    suboptions:
      gateway:
        description:
          - Participant gateway in override VPN domain identified by the name or UID.
        type: str
      vpn_domain:
        description:
          - VPN domain network identified by the name or UID.
        type: str
  permanent_tunnels:
    description:
      - Permanent tunnels properties.
      - Available from R82 JHF management version.
    type: dict
    version_added: "6.5.0"
    suboptions:
      set_permanent_tunnels:
        description:
          - Indicates which tunnels to set as permanent.
        type: str
        choices: ['on all tunnels in the community', 'on all tunnels of specific gateways', 'on specific tunnels in the community', 'off']
      gateways:
        description:
          - List of gateways to set all their tunnels to permanent with specified track options. Will take effect only if set-permanent-tunnels-on
            is set to all-tunnels-of-specific-gateways.
        type: list
        elements: dict
        suboptions:
          gateway:
            description:
              - Gateway to set all is tunnels to permanent with specified track options.<br> Identified by name or UID.
            type: str
          track_options:
            description:
              - Indicates whether to use the community track options or to override track options for the permanent tunnels.
            type: str
            choices: ['according to community track options', 'override track options']
          override_tunnel_down_track:
            description:
              - Gateway tunnel down track option. Relevant only if the track-options is set to 'override track options'.
            type: str
            choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                     'user defined alert no.3']
          override_tunnel_up_track:
            description:
              - Gateway tunnel up track option. Relevant only if the track-options is set to 'override track options'.
            type: str
            choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                     'user defined alert no.3']
      tunnels:
        description:
          - List of tunnels to set as permanent with specified track options. Will take effect only if set-permanent-tunnels-on is set to
            specific-tunnels-in-the-community.
        type: list
        elements: dict
        suboptions:
          first_tunnel_endpoint:
            description:
              - First tunnel endpoint (center gateway). Identified by name or UID.
            type: str
          second_tunnel_endpoint:
            description:
              - Second tunnel endpoint (center gateway for meshed VPN community and satellite gateway for star VPN community). Identified by name or UID.
            type: str
          track_options:
            description:
              - Indicates whether to use the community track options or to override track options for the permanent tunnels.
            type: str
            choices: ['according to community track options', 'override track options']
          override_tunnel_down_track:
            description:
              - Gateway tunnel down track option. Relevant only if the track-options is set to 'override track options'.
            type: str
            choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                     'user defined alert no.3']
          override_tunnel_up_track:
            description:
              - Gateway tunnel up track option. Relevant only if the track-options is set to 'override track options'.
            type: str
            choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                     'user defined alert no.3']
      rim:
        description:
          - Route Injection Mechanism settings.
        type: dict
        suboptions:
          enabled:
            description:
              - Indicates whether Route Injection Mechanism is enabled.
            type: bool
          enable_on_center_gateways:
            description:
              - Indicates whether to enable automatic Route Injection Mechanism on center gateways.
            type: bool
          enable_on_satellite_gateways:
            description:
              - Indicates whether to enable automatic Route Injection Mechanism on satellite gateways.
            type: bool
          route_injection_track:
            description:
              - Route injection track method.
            type: str
            choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                     'user defined alert no.3']
      tunnel_down_track:
        description:
          - VPN community permanent tunnels down track option.
        type: str
        choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                 'user defined alert no.3']
      tunnel_up_track:
        description:
          - Permanent tunnels up track option.
        type: str
        choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                 'user defined alert no.3']
  satellite_gateways:
    description:
      - Collection of Gateway objects representing satellite gateways identified by the name or UID.
    type: list
    elements: str
  shared_secrets:
    description:
      - Shared secrets for external gateways.
      - Available from R80.10 management version.
    type: list
    elements: dict
    suboptions:
      external_gateway:
        description:
          - External gateway identified by the name or UID.
        type: str
      shared_secret:
        description:
          - Shared secret.
        type: str
  tags:
    description:
      - Collection of tag identifiers.
    type: list
    elements: str
  tunnel_granularity:
    description:
      - VPN tunnel sharing option to be used.
      - Available from R81 management version.
    type: str
    choices: ['per_host', 'per_subnet', 'universal']
    version_added: "5.1.0"
  use_shared_secret:
    description:
      - Indicates whether the shared secret should be used for all external gateways.
      - Available from R80.10 management version.
    type: bool
  vpn_routing:
    description:
      - Enable VPN routing to satellites.
      - Available from R82 JHF management version.
    type: str
    choices: ['to center only', 'to center and to other satellites', 'to center other satellites and internet']
    version_added: "6.5.0"
  wire_mode:
    description:
      - VPN Community Wire mode properties.
      - Available from R82 JHF management version.
    type: dict
    version_added: "6.5.0"
    suboptions:
      allow_uninspected_encrypted_traffic:
        description:
          - Allow uninspected encrypted traffic between Wire mode interfaces of this Community members.
        type: bool
      allow_uninspected_encrypted_routing:
        description:
          - Allow members to route uninspected encrypted traffic in VPN routing configurations.
        type: bool
  routing_mode:
    description:
      - VPN Community Routing Mode.
      - Available from R82 JHF management version.
    type: str
    choices: ['domain_based', 'route_based']
    version_added: "6.5.0"
  advanced_properties:
    description:
      - Advanced properties.
      - Available from R82 JHF management version.
    type: dict
    version_added: "6.5.0"
    suboptions:
      support_ip_compression:
        description:
          - Indicates whether to support IP compression.
        type: bool
      use_aggressive_mode:
        description:
          - Indicates whether to use aggressive mode.
        type: bool
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
- name: add-vpn-community-star
  cp_mgmt_vpn_community_star:
    center_gateways: Second_Security_Gateway
    encryption_method: prefer ikev2 but support ikev1
    encryption_suite: custom
    ike_phase_1:
      data_integrity: sha1
      diffie_hellman_group: group 19
      encryption_algorithm: aes-128
    ike_phase_2:
      data_integrity: aes-xcbc
      encryption_algorithm: aes-gcm-128
    name: New_VPN_Community_Star_1
    state: present

- name: set-vpn-community-star
  cp_mgmt_vpn_community_star:
    encryption_method: ikev2 only
    encryption_suite: custom
    ike_phase_1:
      data_integrity: sha1
      diffie_hellman_group: group 19
      encryption_algorithm: aes-128
    ike_phase_2:
      data_integrity: aes-xcbc
      encryption_algorithm: aes-gcm-128
    name: New_VPN_Community_Star_1
    state: present

- name: delete-vpn-community-star
  cp_mgmt_vpn_community_star:
    name: New_VPN_Community_Star_1
    state: absent
"""

RETURN = """
cp_mgmt_vpn_community_star:
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
        center_gateways=dict(type="list", elements="str"),
        disable_nat=dict(
            type="bool"
        ),

        disable_nat_on=dict(
            type="str",
            choices=[
                "satellite gateways only",
                "both center and satellite gateways"
            ]
        ),

        encrypted_traffic=dict(
            type="dict",
            options=dict(
                enabled=dict(type="bool", ),
                community_members=dict(
                    type="str",
                    choices=[
                        "satellite gateways only",
                        "both center and satellite gateways"
                    ]
                )
            )
        ),
        encryption_method=dict(
            type="str",
            choices=[
                "prefer ikev2 but support ikev1",
                "ikev2 only",
                "ikev1 for ipv4 and ikev2 for ipv6 only",
            ],
        ),
        encryption_suite=dict(
            type="str",
            choices=[
                "suite-b-gcm-256",
                "custom",
                "vpn b",
                "vpn a",
                "suite-b-gcm-128",
            ],
        ),
        excluded_services=dict(type="list", elements="str"),
        granular_encryptions=dict(type='list', elements="dict", options=dict(
            internal_gateway=dict(type='str'),
            external_gateway=dict(type='str'),
            encryption_method=dict(type='str', choices=['prefer ikev2 but support ikev1', 'ikev2 only',
                                                        'ikev1 for ipv4 and ikev2 for ipv6 only']),
            encryption_suite=dict(type='str',
                                  choices=['suite-b-gcm-256', 'custom', 'vpn b', 'vpn a', 'suite-b-gcm-128']),
            ike_phase_1=dict(type='dict', options=dict(
                encryption_algorithm=dict(type='str', choices=['cast', 'aes-256', 'des', 'aes-128', '3des']),
                data_integrity=dict(type='str', choices=['aes-xcbc', 'sha1', 'sha256', 'sha384', 'sha512', 'md5']),
                diffie_hellman_group=dict(type='str', choices=['group-1', 'group-2', 'group-5',
                                                               'group-14', 'group-15', 'group-16', 'group-17',
                                                               'group-18', 'group-19', 'group-20',
                                                               'group-24']),
                ike_p1_rekey_time=dict(type='int', no_log=False),
                ike_p1_rekey_time_unit=dict(type='str', choices=['days', 'hours', 'minutes', 'seconds'])
            )),
            ike_phase_2=dict(type='dict', options=dict(
                encryption_algorithm=dict(type='str', choices=['cast', 'aes-gcm-256', 'cast-40',
                                                               'aes-256', 'des', 'aes-128', '3des', 'des-40cp',
                                                               'aes-gcm-128', 'none']),
                data_integrity=dict(type='str', choices=['aes-xcbc', 'sha1', 'sha256', 'sha384', 'sha512', 'md5']),
                ike_p2_use_pfs=dict(type='bool'),
                ike_p2_pfs_dh_grp=dict(type='str', choices=['group-1', 'group-2', 'group-5',
                                                            'group-14', 'group-15', 'group-16', 'group-17', 'group-18',
                                                            'group-19', 'group-20', 'group-24']),
                ike_p2_rekey_time=dict(type='int', no_log=False),
                ike_p2_rekey_time_unit=dict(type='str', choices=['days', 'hours', 'minutes', 'seconds']),
            ))
        )),
        ike_phase_1=dict(
            type="dict",
            options=dict(
                data_integrity=dict(
                    type="str",
                    choices=["aes-xcbc", "sha1", "sha256", "sha384", "sha512", "md5"],
                ),
                diffie_hellman_group=dict(
                    type="str",
                    choices=[
                        "group-1",
                        "group-2",
                        "group-5",
                        "group-14",
                        "group-19",
                        "group-20",
                    ],
                ),
                encryption_algorithm=dict(
                    type="str",
                    choices=["cast", "aes-256", "des", "aes-128", "3des"],
                ),
                ike_p1_rekey_time=dict(type='int', no_log=False),
                ike_p1_rekey_time_unit=dict(type='str', choices=['days', 'hours', 'minutes', 'seconds']),
            ),
        ),
        ike_phase_2=dict(
            type="dict",
            options=dict(
                data_integrity=dict(
                    type="str",
                    choices=["aes-xcbc", "sha1", "sha256", "sha384", "sha512", "md5"],
                ),
                encryption_algorithm=dict(
                    type="str",
                    choices=[
                        "cast",
                        "aes-gcm-256",
                        "cast-40",
                        "aes-256",
                        "des",
                        "aes-128",
                        "3des",
                        "des-40cp",
                        "aes-gcm-128",
                        "none",
                    ],
                ),
                ike_p2_use_pfs=dict(type='bool'),
                ike_p2_pfs_dh_grp=dict(type='str', choices=['group-1', 'group-2', 'group-5', 'group-14',
                                                            'group-15', 'group-16', 'group-17', 'group-18', 'group-19',
                                                            'group-20', 'group-24']),
                ike_p2_rekey_time=dict(type='int', no_log=False),
                ike_p2_rekey_time_unit=dict(type='str', choices=['days', 'hours', 'minutes', 'seconds']),
            ),
        ),
        mep=dict(
            type="dict",
            options=dict(
                enabled=dict(
                    type="bool"
                ),
                entry_point_selection_mechanism=dict(
                    type="str",
                    choices=[
                        "closest gateway to source",
                        "closest gateway to destination",
                        "random selection",
                        "manual"
                    ]
                ),
                entry_point_final_selection_mechanism=dict(
                    type="str",
                    choices=[
                        "random selection",
                        "first to respond"
                    ]
                ),
                tracking=dict(
                    type="str",
                    choices=[
                        "none",
                        "log",
                        "popup alert",
                        "mail alert",
                        "snmp trap alert",
                        "user defined alert no.1",
                        "user defined alert no.2",
                        "user defined alert no.3"
                    ]
                ),
                default_priority_rule=dict(
                    type="dict",
                    options=dict(
                        first_priority_center_gateways=dict(
                            type="list", elements="str"
                        ),
                        second_priority_center_gateways=dict(
                            type="list", elements="str"
                        ),
                        third_priority_center_gateways=dict(
                            type="list", elements="str"
                        )
                    )
                ),
                exception_priority_rules=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        satellite_gateways=dict(
                            type="list", elements="str"
                        ),
                        first_priority_center_gateways=dict(
                            type="list", elements="str"
                        ),
                        second_priority_center_gateways=dict(
                            type="list", elements="str"
                        ),
                        third_priority_center_gateways=dict(
                            type="list", elements="str"
                        )
                    )
                )
            )
        ),
        mesh_center_gateways=dict(type="bool"),
        permanent_tunnels=dict(
            type="dict",
            options=dict(
                set_permanent_tunnels=dict(
                    type="str",
                    choices=[
                        "on all tunnels in the community",
                        "on all tunnels of specific gateways",
                        "on specific tunnels in the community",
                        "off"
                    ]
                ),
                gateways=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        gateway=dict(
                            type="str"
                        ),
                        track_options=dict(
                            type="str",
                            choices=[
                                "according to community track options",
                                "override track options"
                            ]
                        ),
                        override_tunnel_down_track=dict(
                            type="str",
                            choices=[
                                "none",
                                "log",
                                "popup alert",
                                "mail alert",
                                "snmp trap alert",
                                "user defined alert no.1",
                                "user defined alert no.2",
                                "user defined alert no.3"
                            ]
                        ),
                        override_tunnel_up_track=dict(
                            type="str",
                            choices=[
                                "none",
                                "log",
                                "popup alert",
                                "mail alert",
                                "snmp trap alert",
                                "user defined alert no.1",
                                "user defined alert no.2",
                                "user defined alert no.3"
                            ]
                        )
                    )
                ),
                tunnels=dict(
                    type="list",
                    elements="dict",
                    options=dict(
                        first_tunnel_endpoint=dict(
                            type="str"
                        ),
                        second_tunnel_endpoint=dict(
                            type="str"
                        ),
                        track_options=dict(
                            type="str",
                            choices=[
                                "according to community track options",
                                "override track options"
                            ]
                        ),
                        override_tunnel_down_track=dict(
                            type="str",
                            choices=[
                                "none",
                                "log",
                                "popup alert",
                                "mail alert",
                                "snmp trap alert",
                                "user defined alert no.1",
                                "user defined alert no.2",
                                "user defined alert no.3"
                            ]
                        ),
                        override_tunnel_up_track=dict(
                            type="str",
                            choices=[
                                "none",
                                "log",
                                "popup alert",
                                "mail alert",
                                "snmp trap alert",
                                "user defined alert no.1",
                                "user defined alert no.2",
                                "user defined alert no.3"
                            ]
                        )
                    )
                ),
                rim=dict(
                    type="dict",
                    options=dict(
                        enabled=dict(
                            type="bool"
                        ),
                        enable_on_center_gateways=dict(
                            type="bool"
                        ),
                        enable_on_satellite_gateways=dict(
                            type="bool"
                        ),
                        route_injection_track=dict(
                            type="str",
                            choices=[
                                "none",
                                "log",
                                "popup alert",
                                "mail alert",
                                "snmp trap alert",
                                "user defined alert no.1",
                                "user defined alert no.2",
                                "user defined alert no.3"
                            ]
                        )
                    )
                ),
                tunnel_down_track=dict(
                    type="str",
                    choices=[
                        "none",
                        "log",
                        "popup alert",
                        "mail alert",
                        "snmp trap alert",
                        "user defined alert no.1",
                        "user defined alert no.2",
                        "user defined alert no.3"
                    ]
                ),
                tunnel_up_track=dict(
                    type="str",
                    choices=[
                        "none",
                        "log",
                        "popup alert",
                        "mail alert",
                        "snmp trap alert",
                        "user defined alert no.1",
                        "user defined alert no.2",
                        "user defined alert no.3"
                    ]
                )
            )
        ),
        override_vpn_domains=dict(type='list', elements="dict", options=dict(
            gateway=dict(type='str'),
            vpn_domain=dict(type='str')
        )),
        satellite_gateways=dict(type="list", elements="str"),
        shared_secrets=dict(
            type="list",
            elements="dict",
            no_log=True,
            options=dict(
                external_gateway=dict(type="str"),
                shared_secret=dict(type="str", no_log=True),
            ),
        ),
        tags=dict(type="list", elements="str"),
        tunnel_granularity=dict(type='str', choices=['per_host', 'per_subnet', 'universal']),
        use_shared_secret=dict(type="bool"),
        vpn_routing=dict(
            type="str",
            choices=[
                "to center only",
                "to center and to other satellites",
                "to center other satellites and internet"
            ]
        ),

        wire_mode=dict(
            type="dict",
            options=dict(
                allow_uninspected_encrypted_traffic=dict(
                    type="bool"
                ),
                allow_uninspected_encrypted_routing=dict(
                    type="bool"
                )
            )
        ),

        routing_mode=dict(
            type="str",
            choices=[
                "domain_based",
                "route_based"
            ]
        ),

        advanced_properties=dict(
            type="dict",
            options=dict(
                support_ip_compression=dict(
                    type="bool"
                ),
                use_aggressive_mode=dict(
                    type="bool"
                )
            )
        ),
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
    api_call_object = "vpn-community-star"

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
