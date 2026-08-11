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
module: cp_mgmt_simple_gateway
short_description: Manages simple-gateway objects on Check Point over Web Services API
description:
  - Manages simple-gateway objects on Check Point devices including creating, updating and removing objects.
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
  ip_address:
    description:
      - IPv4 or IPv6 address. If both addresses are required use ipv4-address and ipv6-address fields explicitly.
    type: str
  ipv4_address:
    description:
      - IPv4 address.
    type: str
  ipv6_address:
    description:
      - IPv6 address.
    type: str
  anti_bot:
    description:
      - Anti-Bot blade enabled.
    type: bool
  anti_virus:
    description:
      - Anti-Virus blade enabled.
    type: bool
  application_control:
    description:
      - Application Control blade enabled.
    type: bool
  content_awareness:
    description:
      - Content Awareness blade enabled.
      - Available from R80.10 management version.
    type: bool
  enable_https_inspection:
    description:
      - Enable HTTPS Inspection after defining an outbound inspection certificate. <br>To define the outbound certificate use outbound inspection
        certificate API.
    type: bool
  firewall:
    description:
      - Firewall blade enabled.
    type: bool
  firewall_settings:
    description:
      - N/A
    type: dict
    suboptions:
      auto_calculate_connections_hash_table_size_and_memory_pool:
        description:
          - N/A
        type: bool
      auto_maximum_limit_for_concurrent_connections:
        description:
          - N/A
        type: bool
      connections_hash_size:
        description:
          - N/A
        type: int
      maximum_limit_for_concurrent_connections:
        description:
          - N/A
        type: int
      maximum_memory_pool_size:
        description:
          - N/A
        type: int
      memory_pool_size:
        description:
          - N/A
        type: int
  identity_awareness:
    description:
      - Identity awareness blade enabled.
    type: bool
    version_added: "7.0.0"
  identity_awareness_settings:
    description:
      - Gateway Identity Awareness settings.
    type: dict
    version_added: "7.0.0"
    suboptions:
      browser_based_authentication:
        description:
          - Enable Browser Based Authentication source.
        type: bool
      browser_based_authentication_settings:
        description:
          - Browser Based Authentication settings.
        type: dict
        suboptions:
          authentication_settings:
            description:
              - Authentication Settings for Browser Based Authentication.
            type: dict
            suboptions:
              authentication_method:
                description:
                  - Authentication method.
                type: str
                choices: ['username and password', 'defined on user record', 'identity provider', 'radius']
              identity_provider:
                description:
                  - Identity provider object identified by the name or UID. Must be set when "authentication-method" was selected to be "identity provider".
                type: list
                elements: str
              radius:
                description:
                  - Radius server object identified by the name or UID. Must be set when "authentication-method" was selected to be "radius".
                type: str
              users_directories:
                description:
                  - Users directories.
                type: dict
                suboptions:
                  external_user_profile:
                    description:
                      - External user profile.
                    type: bool
                  internal_users:
                    description:
                      - Internal users.
                    type: bool
                  users_from_external_directories:
                    description:
                      - Users from external directories.
                    type: str
                    choices: ['all gateways directories', 'specific', 'none']
                  specific:
                    description:
                      - LDAP AU objects identified by the name or UID. Must be set when "users-from-external-directories" was selected to be "specific".
                    type: list
                    elements: str
          browser_based_authentication_portal_settings:
            description:
              - Browser Based Authentication portal settings.
            type: dict
            suboptions:
              portal_web_settings:
                description:
                  - Configuration of the portal web settings.
                type: dict
                suboptions:
                  aliases:
                    description:
                      - List of URL aliases that are redirected to the main portal URL.
                    type: list
                    elements: str
                  ip_address:
                    description:
                      - Optional, IP address for the web portal to use, if your DNS server fails to resolve the main portal URL.
                        Note, If your DNS server resolves the main portal URL, this IP address is ignored.
                    type: str
                  main_url:
                    description:
                      - The main URL for the web portal.
                    type: str
              certificate_settings:
                description:
                  - Configuration of the portal certificate settings.
                type: dict
                suboptions:
                  base64_certificate:
                    description:
                      - The certificate file encoded in Base64 with padding.
                        This file must be in the *.p12 format.
                    type: str
                  base64_password:
                    description:
                      - Password (encoded in Base64 with padding) for the certificate file.
                    type: str
              accessibility:
                description:
                  - Configuration of the portal access settings.
                type: dict
                suboptions:
                  allow_access_from:
                    description:
                      - Allowed access to the web portal (based on interfaces, or security policy).
                    type: str
                    choices: ['rule_base', 'internal_interfaces', 'all_interfaces']
                  internal_access_settings:
                    description:
                      - Configuration of the additional portal access settings for internal interfaces only.
                    type: dict
                    suboptions:
                      undefined:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'Undefined'.
                        type: bool
                      dmz:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'DMZ'.
                        type: bool
                      vpn:
                        description:
                          - Controls portal access settings for interfaces that are part of a VPN Encryption Domain.
                        type: bool
      identity_agent:
        description:
          - Enable Identity Agent source.
        type: bool
      identity_agent_settings:
        description:
          - Identity Agent settings.
        type: dict
        suboptions:
          agents_interval_keepalive:
            description:
              - Agents send keepalive period (minutes).
            type: int
          user_reauthenticate_interval:
            description:
              - Agent reauthenticate time interval (minutes).
            type: int
          authentication_settings:
            description:
              - Authentication Settings for Identity Agent.
            type: dict
            suboptions:
              authentication_method:
                description:
                  - Authentication method.
                type: str
                choices: ['username and password', 'defined on user record', 'radius']
              radius:
                description:
                  - Radius server object identified by the name or UID. Must be set when "authentication-method" was selected to be "radius".
                type: str
              users_directories:
                description:
                  - Users directories.
                type: dict
                suboptions:
                  external_user_profile:
                    description:
                      - External user profile.
                    type: bool
                  internal_users:
                    description:
                      - Internal users.
                    type: bool
                  users_from_external_directories:
                    description:
                      - Users from external directories.
                    type: str
                    choices: ['all gateways directories', 'specific', 'none']
                  specific:
                    description:
                      - LDAP AU objects identified by the name or UID. Must be set when "users-from-external-directories" was selected to be "specific".
                    type: list
                    elements: str
          identity_agent_portal_settings:
            description:
              - Identity Agent accessibility settings.
            type: dict
            suboptions:
              accessibility:
                description:
                  - Configuration of the portal access settings.
                type: dict
                suboptions:
                  allow_access_from:
                    description:
                      - Allowed access to the web portal (based on interfaces, or security policy).
                    type: str
                    choices: ['rule_base', 'internal_interfaces', 'all_interfaces']
                  internal_access_settings:
                    description:
                      - Configuration of the additional portal access settings for internal interfaces only.
                    type: dict
                    suboptions:
                      undefined:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'Undefined'.
                        type: bool
                      dmz:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'DMZ'.
                        type: bool
                      vpn:
                        description:
                          - Controls portal access settings for interfaces that are part of a VPN Encryption Domain.
                        type: bool
      identity_based_enforcement:
        description:
          - ON, Configures this object as a PEP-only object - identity-based enforcement (PEP) is enabled.<br>OFF, Configures this object as a
            PDP-only object - identity-based enforcement is disabled.
        type: str
        choices: ['on', 'off']
      identity_collector:
        description:
          - Enable Identity Collector source.
        type: bool
      identity_collector_settings:
        description:
          - Identity Collector settings.
        type: dict
        suboptions:
          authentication_settings:
            description:
              - Authentication Settings for Identity Collector.
            type: dict
            suboptions:
              users_directories:
                description:
                  - Users directories.
                type: dict
                suboptions:
                  external_user_profile:
                    description:
                      - External user profile.
                    type: bool
                  internal_users:
                    description:
                      - Internal users.
                    type: bool
                  users_from_external_directories:
                    description:
                      - Users from external directories.
                    type: str
                    choices: ['all gateways directories', 'specific', 'none']
                  specific:
                    description:
                      - LDAP AU objects identified by the name or UID. Must be set when "users-from-external-directories" was selected to be "specific".
                    type: list
                    elements: str
          authorized_clients:
            description:
              - Authorized Clients.
            type: list
            elements: dict
            suboptions:
              client:
                description:
                  - Host / Network Group Name or UID.
                type: str
              client_secret:
                description:
                  - Client Secret.
                type: str
          client_access_permissions:
            description:
              - Identity Collector accessibility settings.
            type: dict
            suboptions:
              accessibility:
                description:
                  - Configuration of the portal access settings.
                type: dict
                suboptions:
                  allow_access_from:
                    description:
                      - Allowed access to the web portal (based on interfaces, or security policy).
                    type: str
                    choices: ['rule_base', 'internal_interfaces', 'all_interfaces']
                  internal_access_settings:
                    description:
                      - Configuration of the additional portal access settings for internal interfaces only.
                    type: dict
                    suboptions:
                      undefined:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'Undefined'.
                        type: bool
                      dmz:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'DMZ'.
                        type: bool
                      vpn:
                        description:
                          - Controls portal access settings for interfaces that are part of a VPN Encryption Domain.
                        type: bool
      identity_sharing_settings:
        description:
          - Identity sharing settings.
        type: dict
        suboptions:
          share_with_other_gateways:
            description:
              - Enable identity sharing with other gateways.
            type: bool
          receive_from_infinity_identity:
            description:
              - Enable receiving identities from Infinity Identity.
            type: bool
          receive_from_other_gateways:
            description:
              - Enable receiving identity from other gateways.
            type: bool
          receive_from:
            description:
              - Gateway(s) to receive identity from.
            type: list
            elements: str
          cache_mode:
            description:
              - True, In case of connectivity loss from the Policy-Decision-Point (PDP), extend Identity cache up-to
                "cache-mode-duration".<br>False, Identity Cache Mode is disabled, in case of connectivity loss from the Policy-Decision-Point, existing
                Identities will be lost immediately.
            type: dict
            suboptions:
              override_profile:
                description:
                  - Override profile of global configuration.
                type: bool
              value:
                description:
                  - Override value.<br><font color="red">Required only for</font> 'override-profile' is True.
                type: bool
          cache_mode_duration:
            description:
              - Time limit for keeping Identities in the cache.
            type: dict
            suboptions:
              override_profile:
                description:
                  - Override profile of global configuration.
                type: bool
              value:
                description:
                  - Override value.<br><font color="red">Required only for</font> 'override-profile' is True.
                    Valid values are in the range 1-2880.
                type: int
          scaled_sharing:
            description:
              - Enable Scaled Sharing.
            type: bool
      identity_web_api:
        description:
          - Enable Identity Web API source.
        type: bool
      identity_web_api_settings:
        description:
          - Identity Web API settings.
        type: dict
        suboptions:
          authentication_settings:
            description:
              - Authentication Settings for Identity Web Api.
            type: dict
            suboptions:
              users_directories:
                description:
                  - Users directories.
                type: dict
                suboptions:
                  external_user_profile:
                    description:
                      - External user profile.
                    type: bool
                  internal_users:
                    description:
                      - Internal users.
                    type: bool
                  users_from_external_directories:
                    description:
                      - Users from external directories.
                    type: str
                    choices: ['all gateways directories', 'specific', 'none']
                  specific:
                    description:
                      - LDAP AU objects identified by the name or UID. Must be set when "users-from-external-directories" was selected to be "specific".
                    type: list
                    elements: str
          authorized_clients:
            description:
              - Authorized Clients.
            type: list
            elements: dict
            suboptions:
              client:
                description:
                  - Host / Network Group Name or UID.
                type: str
              client_secret:
                description:
                  - Client Secret.
                type: str
          client_access_permissions:
            description:
              - Identity Web Api accessibility settings.
            type: dict
            suboptions:
              accessibility:
                description:
                  - Configuration of the portal access settings.
                type: dict
                suboptions:
                  allow_access_from:
                    description:
                      - Allowed access to the web portal (based on interfaces, or security policy).
                    type: str
                    choices: ['rule_base', 'internal_interfaces', 'all_interfaces']
                  internal_access_settings:
                    description:
                      - Configuration of the additional portal access settings for internal interfaces only.
                    type: dict
                    suboptions:
                      undefined:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'Undefined'.
                        type: bool
                      dmz:
                        description:
                          - Controls portal access settings for internal interfaces, whose topology is set to 'DMZ'.
                        type: bool
                      vpn:
                        description:
                          - Controls portal access settings for interfaces that are part of a VPN Encryption Domain.
                        type: bool
      proxy_settings:
        description:
          - Identity-Awareness Proxy settings.
        type: dict
        suboptions:
          detect_using_x_forward_for:
            description:
              - Whether to use X-Forward-For HTTP header, which is added by the proxy server to keep track of the original source IP.
            type: bool
      remote_access:
        description:
          - Enable Remote Access Identity source.
        type: bool
  interfaces:
    description:
      - Network interfaces. When a gateway is updated with a new interfaces, the existing interfaces are removed.
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Object name.
        type: str
      anti_spoofing:
        description:
          - N/A
        type: bool
      anti_spoofing_settings:
        description:
          - N/A
        type: dict
        suboptions:
          action:
            description:
              - If packets will be rejected (the Prevent option) or whether the packets will be monitored (the Detect option).
            type: str
            choices: ['prevent', 'detect']
      ip_address:
        description:
          - IPv4 or IPv6 address. If both addresses are required use ipv4-address and ipv6-address fields explicitly.
        type: str
      ipv4_address:
        description:
          - IPv4 address.
        type: str
      ipv6_address:
        description:
          - IPv6 address.
        type: str
      network_mask:
        description:
          - IPv4 or IPv6 network mask. If both masks are required use ipv4-network-mask and ipv6-network-mask fields explicitly. Instead of
            providing mask itself it is possible to specify IPv4 or IPv6 mask length in mask-length field. If both masks length are required use
            ipv4-mask-length and  ipv6-mask-length fields explicitly.
        type: str
      ipv4_network_mask:
        description:
          - IPv4 network address.
        type: str
      ipv6_network_mask:
        description:
          - IPv6 network address.
        type: str
      mask_length:
        description:
          - IPv4 or IPv6 network mask length.
        type: str
      ipv4_mask_length:
        description:
          - IPv4 network mask length.
        type: str
      ipv6_mask_length:
        description:
          - IPv6 network mask length.
        type: str
      security_zone:
        description:
          - N/A
        type: bool
      security_zone_settings:
        description:
          - N/A
        type: dict
        suboptions:
          auto_calculated:
            description:
              - Security Zone is calculated according to where the interface leads to.
            type: bool
          specific_zone:
            description:
              - Security Zone specified manually.
            type: str
      tags:
        description:
          - Collection of tag identifiers.
        type: list
        elements: str
      topology:
        description:
          - N/A
        type: str
        choices: ['automatic', 'external', 'internal']
      topology_settings:
        description:
          - N/A
        type: dict
        suboptions:
          interface_leads_to_dmz:
            description:
              - Whether this interface leads to demilitarized zone (perimeter network).
            type: bool
          ip_address_behind_this_interface:
            description:
              - N/A
            type: str
            choices: ['not defined', 'network defined by the interface ip and net mask', 'network defined by routing', 'specific']
          specific_network:
            description:
              - Network behind this interface.
            type: str
      color:
        description:
          - Color of the object. Should be one of existing colors.
        type: str
        choices: ['aquamarine', 'black', 'blue', 'crete blue', 'burlywood', 'cyan', 'dark green', 'khaki', 'orchid', 'dark orange',
                 'dark sea green', 'pink', 'turquoise', 'dark blue', 'firebrick', 'brown', 'forest green', 'gold', 'dark gold', 'gray', 'dark gray',
                 'light green', 'lemon chiffon', 'coral', 'sea green', 'sky blue', 'magenta', 'purple', 'slate blue', 'violet red', 'navy blue', 'olive',
                 'orange', 'red', 'sienna', 'yellow']
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
  ips:
    description:
      - Intrusion Prevention System blade enabled.
    type: bool
  ips_settings:
    description:
      - Gateway IPS settings.
      - Available from R82 JHF management version.
    type: dict
    version_added: "6.5.0"
    suboptions:
      bypass_all_under_load:
        description:
          - Disable/enable all IPS protections until CPU and memory levels are back to normal.
        type: bool
      bypass_track_method:
        description:
          - Track options when all IPS protections are disabled until CPU/memory levels are back to normal.
        type: str
        choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                 'user defined alert no.3']
      activation_mode:
        description:
          - Defines whether the IPS blade operates in Detect Only mode or enforces the configured IPS Policy.
        type: str
        choices: ['according-to-policy', 'detect-only']
      cpu_usage_low_threshold:
        description:
          - CPU usage low threshold percentage (1-99).
        type: int
      cpu_usage_high_threshold:
        description:
          - CPU usage high threshold percentage (1-99).
        type: int
      memory_usage_low_threshold:
        description:
          - Memory usage low threshold percentage (1-99).
        type: int
      memory_usage_high_threshold:
        description:
          - Memory usage high threshold percentage (1-99).
        type: int
      send_threat_cloud_info:
        description:
          - Help improve Check Point Threat Prevention product by sending anonymous information.
        type: bool
  logs_settings:
    description:
      - N/A
    type: dict
    suboptions:
      alert_when_free_disk_space_below:
        description:
          - N/A
        type: bool
      alert_when_free_disk_space_below_threshold:
        description:
          - N/A
        type: int
      alert_when_free_disk_space_below_type:
        description:
          - N/A
        type: str
        choices: ['none', 'log', 'popup alert', 'mail alert', 'snmp trap alert', 'user defined alert no.1', 'user defined alert no.2',
                 'user defined alert no.3']
      before_delete_keep_logs_from_the_last_days:
        description:
          - N/A
        type: bool
      before_delete_keep_logs_from_the_last_days_threshold:
        description:
          - N/A
        type: int
      before_delete_run_script:
        description:
          - N/A
        type: bool
      before_delete_run_script_command:
        description:
          - N/A
        type: str
      delete_index_files_older_than_days:
        description:
          - N/A
        type: bool
      delete_index_files_older_than_days_threshold:
        description:
          - N/A
        type: int
      delete_index_files_when_index_size_above:
        description:
          - N/A
        type: bool
      delete_index_files_when_index_size_above_threshold:
        description:
          - N/A
        type: int
      delete_when_free_disk_space_below:
        description:
          - N/A
        type: bool
      delete_when_free_disk_space_below_threshold:
        description:
          - N/A
        type: int
      detect_new_citrix_ica_application_names:
        description:
          - N/A
        type: bool
      distribute_logs_between_all_active_servers:
        description:
          - Distribute logs between all active servers.
        type: bool
        version_added: "7.0.0"
      forward_logs_to_log_server:
        description:
          - N/A
        type: bool
      forward_logs_to_log_server_name:
        description:
          - N/A
        type: str
      forward_logs_to_log_server_schedule_name:
        description:
          - N/A
        type: str
      free_disk_space_metrics:
        description:
          - N/A
        type: str
        choices: ['mbytes', 'percent']
      perform_log_rotate_before_log_forwarding:
        description:
          - N/A
        type: bool
      reject_connections_when_free_disk_space_below_threshold:
        description:
          - N/A
        type: bool
      reserve_for_packet_capture_metrics:
        description:
          - N/A
        type: str
        choices: ['percent', 'mbytes']
      reserve_for_packet_capture_threshold:
        description:
          - N/A
        type: int
      rotate_log_by_file_size:
        description:
          - N/A
        type: bool
      rotate_log_file_size_threshold:
        description:
          - N/A
        type: int
      rotate_log_on_schedule:
        description:
          - N/A
        type: bool
      rotate_log_schedule_name:
        description:
          - N/A
        type: str
      stop_logging_when_free_disk_space_below:
        description:
          - N/A
        type: bool
      stop_logging_when_free_disk_space_below_threshold:
        description:
          - N/A
        type: int
      turn_on_qos_logging:
        description:
          - N/A
        type: bool
      update_account_log_every:
        description:
          - N/A
        type: int
  one_time_password:
    description:
      - N/A
    type: str
  os_name:
    description:
      - Gateway platform operating system.
    type: str
  save_logs_locally:
    description:
      - Save logs locally on the gateway.
    type: bool
  send_alerts_to_server:
    description:
      - Server(s) to send alerts to.
    type: list
    elements: str
  send_logs_to_backup_server:
    description:
      - Backup server(s) to send logs to.
    type: list
    elements: str
  send_logs_to_server:
    description:
      - Server(s) to send logs to.
    type: list
    elements: str
  tags:
    description:
      - Collection of tag identifiers.
    type: list
    elements: str
  threat_emulation:
    description:
      - Threat Emulation blade enabled.
    type: bool
  threat_extraction:
    description:
      - Threat Extraction blade enabled.
      - Available from R80.20.M2 management version.
    type: bool
  url_filtering:
    description:
      - URL Filtering blade enabled.
    type: bool
  gateway_version:
    description:
      - Gateway platform version.
    type: str
  vpn:
    description:
      - VPN blade enabled.
    type: bool
  vpn_settings:
    description:
      - Gateway VPN settings.
    type: dict
    suboptions:
      maximum_concurrent_ike_negotiations:
        description:
          - N/A
        type: int
      maximum_concurrent_tunnels:
        description:
          - N/A
        type: int
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
  groups:
    description:
      - Collection of group identifiers.
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
extends_documentation_fragment: check_point.mgmt.checkpoint_objects
"""

EXAMPLES = """
- name: add-simple-gateway
  cp_mgmt_simple_gateway:
    ip_address: 192.0.2.1
    name: gw1
    state: present

- name: set-simple-gateway
  cp_mgmt_simple_gateway:
    anti_bot: true
    anti_virus: true
    application_control: true
    ips: true
    name: test_gateway
    state: present
    threat_emulation: true
    url_filtering: true

- name: delete-simple-gateway
  cp_mgmt_simple_gateway:
    name: gw1
    state: absent
"""

RETURN = """
cp_mgmt_simple_gateway:
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
        ip_address=dict(type="str"),
        ipv4_address=dict(type="str"),
        ipv6_address=dict(type="str"),
        anti_bot=dict(type="bool"),
        anti_virus=dict(type="bool"),
        application_control=dict(type="bool"),
        content_awareness=dict(type="bool"),
        enable_https_inspection=dict(type="bool"),
        firewall=dict(type="bool"),
        firewall_settings=dict(
            type="dict",
            options=dict(
                auto_calculate_connections_hash_table_size_and_memory_pool=dict(
                    type="bool"
                ),
                auto_maximum_limit_for_concurrent_connections=dict(
                    type="bool"
                ),
                connections_hash_size=dict(type="int"),
                maximum_limit_for_concurrent_connections=dict(type="int"),
                maximum_memory_pool_size=dict(type="int"),
                memory_pool_size=dict(type="int"),
            ),
        ),
        identity_awareness=dict(type="bool"),
        identity_awareness_settings=dict(type="dict", options=dict(
            browser_based_authentication=dict(type="bool"),
            browser_based_authentication_settings=dict(type="dict", options=dict(
                authentication_settings=dict(type="dict", options=dict(
                    authentication_method=dict(type="str", choices=["username and password", "defined on user record", "identity provider", "radius"]),
                    identity_provider=dict(type="list", elements="str"),
                    radius=dict(type="str"),
                    users_directories=dict(type="dict", options=dict(
                        external_user_profile=dict(type="bool"),
                        internal_users=dict(type="bool"),
                        users_from_external_directories=dict(type="str", choices=["all gateways directories", "specific", "none"]),
                        specific=dict(type="list", elements="str")
                    ))
                )),
                browser_based_authentication_portal_settings=dict(type="dict", options=dict(
                    portal_web_settings=dict(type="dict", options=dict(
                        aliases=dict(type="list", elements="str"),
                        ip_address=dict(type="str"),
                        main_url=dict(type="str")
                    )),
                    certificate_settings=dict(type="dict", options=dict(
                        base64_certificate=dict(type="str"),
                        base64_password=dict(type="str", no_log=True)
                    )),
                    accessibility=dict(type="dict", options=dict(
                        allow_access_from=dict(type="str", choices=["rule_base", "internal_interfaces", "all_interfaces"]),
                        internal_access_settings=dict(type="dict", options=dict(
                            undefined=dict(type="bool"),
                            dmz=dict(type="bool"),
                            vpn=dict(type="bool")
                        ))
                    ))
                ))
            )),
            identity_agent=dict(type="bool"),
            identity_agent_settings=dict(type="dict", options=dict(
                agents_interval_keepalive=dict(type="int"),
                user_reauthenticate_interval=dict(type="int"),
                authentication_settings=dict(type="dict", options=dict(
                    authentication_method=dict(type="str", choices=["username and password", "defined on user record", "radius"]),
                    radius=dict(type="str"),
                    users_directories=dict(type="dict", options=dict(
                        external_user_profile=dict(type="bool"),
                        internal_users=dict(type="bool"),
                        users_from_external_directories=dict(type="str", choices=["all gateways directories", "specific", "none"]),
                        specific=dict(type="list", elements="str")
                    ))
                )),
                identity_agent_portal_settings=dict(type="dict", options=dict(
                    accessibility=dict(type="dict", options=dict(
                        allow_access_from=dict(type="str", choices=["rule_base", "internal_interfaces", "all_interfaces"]),
                        internal_access_settings=dict(type="dict", options=dict(
                            undefined=dict(type="bool"),
                            dmz=dict(type="bool"),
                            vpn=dict(type="bool")
                        ))
                    ))
                ))
            )),
            identity_based_enforcement=dict(type="str", choices=["on", "off"]),
            identity_collector=dict(type="bool"),
            identity_collector_settings=dict(type="dict", options=dict(
                authentication_settings=dict(type="dict", options=dict(
                    users_directories=dict(type="dict", options=dict(
                        external_user_profile=dict(type="bool"),
                        internal_users=dict(type="bool"),
                        users_from_external_directories=dict(type="str", choices=["all gateways directories", "specific", "none"]),
                        specific=dict(type="list", elements="str")
                    ))
                )),
                authorized_clients=dict(type="list", elements="dict", options=dict(
                    client=dict(type="str"),
                    client_secret=dict(type="str", no_log=True)
                )),
                client_access_permissions=dict(type="dict", options=dict(
                    accessibility=dict(type="dict", options=dict(
                        allow_access_from=dict(type="str", choices=["rule_base", "internal_interfaces", "all_interfaces"]),
                        internal_access_settings=dict(type="dict", options=dict(
                            undefined=dict(type="bool"),
                            dmz=dict(type="bool"),
                            vpn=dict(type="bool")
                        ))
                    ))
                ))
            )),
            identity_sharing_settings=dict(type="dict", options=dict(
                share_with_other_gateways=dict(type="bool"),
                receive_from_infinity_identity=dict(type="bool"),
                receive_from_other_gateways=dict(type="bool"),
                receive_from=dict(type="list", elements="str"),
                cache_mode=dict(type="dict", options=dict(
                    override_profile=dict(type="bool"),
                    value=dict(type="bool")
                )),
                cache_mode_duration=dict(type="dict", options=dict(
                    override_profile=dict(type="bool"),
                    value=dict(type="int")
                )),
                scaled_sharing=dict(type="bool")
            )),
            identity_web_api=dict(type="bool"),
            identity_web_api_settings=dict(type="dict", options=dict(
                authentication_settings=dict(type="dict", options=dict(
                    users_directories=dict(type="dict", options=dict(
                        external_user_profile=dict(type="bool"),
                        internal_users=dict(type="bool"),
                        users_from_external_directories=dict(type="str", choices=["all gateways directories", "specific", "none"]),
                        specific=dict(type="list", elements="str")
                    ))
                )),
                authorized_clients=dict(type="list", elements="dict", options=dict(
                    client=dict(type="str"),
                    client_secret=dict(type="str", no_log=True)
                )),
                client_access_permissions=dict(type="dict", options=dict(
                    accessibility=dict(type="dict", options=dict(
                        allow_access_from=dict(type="str", choices=["rule_base", "internal_interfaces", "all_interfaces"]),
                        internal_access_settings=dict(type="dict", options=dict(
                            undefined=dict(type="bool"),
                            dmz=dict(type="bool"),
                            vpn=dict(type="bool")
                        ))
                    ))
                ))
            )),
            proxy_settings=dict(type="dict", options=dict(
                detect_using_x_forward_for=dict(type="bool")
            )),
            remote_access=dict(type="bool")
        )),
        interfaces=dict(
            type="list",
            elements="dict",
            options=dict(
                name=dict(type="str"),
                anti_spoofing=dict(type="bool"),
                anti_spoofing_settings=dict(
                    type="dict",
                    options=dict(
                        action=dict(type="str", choices=["prevent", "detect"])
                    ),
                ),
                ip_address=dict(type="str"),
                ipv4_address=dict(type="str"),
                ipv6_address=dict(type="str"),
                network_mask=dict(type="str"),
                ipv4_network_mask=dict(type="str"),
                ipv6_network_mask=dict(type="str"),
                mask_length=dict(type="str"),
                ipv4_mask_length=dict(type="str"),
                ipv6_mask_length=dict(type="str"),
                security_zone=dict(type="bool"),
                security_zone_settings=dict(
                    type="dict",
                    options=dict(
                        auto_calculated=dict(type="bool"),
                        specific_zone=dict(type="str"),
                    ),
                ),
                tags=dict(type="list", elements="str"),
                topology=dict(
                    type="str", choices=["automatic", "external", "internal"]
                ),
                topology_settings=dict(
                    type="dict",
                    options=dict(
                        interface_leads_to_dmz=dict(type="bool"),
                        ip_address_behind_this_interface=dict(
                            type="str",
                            choices=[
                                "not defined",
                                "network defined by the interface ip and net mask",
                                "network defined by routing",
                                "specific",
                            ],
                        ),
                        specific_network=dict(type="str"),
                    ),
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
                details_level=dict(
                    type="str", choices=["uid", "standard", "full"]
                ),
                ignore_warnings=dict(type="bool"),
                ignore_errors=dict(type="bool"),
            ),
        ),
        ips=dict(type="bool"),
        ips_settings=dict(
            type="dict",
            options=dict(
                bypass_all_under_load=dict(type="bool"),
                bypass_track_method=dict(type="str",
                                         choices=[
                                             "none",
                                             "log",
                                             "popup alert",
                                             "mail alert",
                                             "snmp trap alert",
                                             "user defined alert no.1",
                                             "user defined alert no.2",
                                             "user defined alert no.3",
                                         ],
                                         ),
                activation_mode=dict(
                    type="str",
                    choices=["according-to-policy", "detect-only"],
                ),
                cpu_usage_low_threshold=dict(type="int"),
                cpu_usage_high_threshold=dict(type="int"),
                memory_usage_low_threshold=dict(type="int"),
                memory_usage_high_threshold=dict(type="int"),
                send_threat_cloud_info=dict(type="bool"),
            ),
        ),
        logs_settings=dict(
            type="dict",
            options=dict(
                alert_when_free_disk_space_below=dict(type="bool"),
                alert_when_free_disk_space_below_threshold=dict(type="int"),
                alert_when_free_disk_space_below_type=dict(
                    type="str",
                    choices=[
                        "none",
                        "log",
                        "popup alert",
                        "mail alert",
                        "snmp trap alert",
                        "user defined alert no.1",
                        "user defined alert no.2",
                        "user defined alert no.3",
                    ],
                ),
                before_delete_keep_logs_from_the_last_days=dict(type="bool"),
                before_delete_keep_logs_from_the_last_days_threshold=dict(
                    type="int"
                ),
                before_delete_run_script=dict(type="bool"),
                before_delete_run_script_command=dict(type="str"),
                delete_index_files_older_than_days=dict(type="bool"),
                delete_index_files_older_than_days_threshold=dict(type="int"),
                delete_index_files_when_index_size_above=dict(type="bool"),
                delete_index_files_when_index_size_above_threshold=dict(
                    type="int"
                ),
                delete_when_free_disk_space_below=dict(type="bool"),
                delete_when_free_disk_space_below_threshold=dict(type="int"),
                detect_new_citrix_ica_application_names=dict(type="bool"),
                distribute_logs_between_all_active_servers=dict(type="bool"),
                forward_logs_to_log_server=dict(type="bool"),
                forward_logs_to_log_server_name=dict(type="str"),
                forward_logs_to_log_server_schedule_name=dict(type="str"),
                free_disk_space_metrics=dict(
                    type="str", choices=["mbytes", "percent"]
                ),
                perform_log_rotate_before_log_forwarding=dict(type="bool"),
                reject_connections_when_free_disk_space_below_threshold=dict(
                    type="bool"
                ),
                reserve_for_packet_capture_metrics=dict(
                    type="str", choices=["percent", "mbytes"]
                ),
                reserve_for_packet_capture_threshold=dict(type="int"),
                rotate_log_by_file_size=dict(type="bool"),
                rotate_log_file_size_threshold=dict(type="int"),
                rotate_log_on_schedule=dict(type="bool"),
                rotate_log_schedule_name=dict(type="str"),
                stop_logging_when_free_disk_space_below=dict(type="bool"),
                stop_logging_when_free_disk_space_below_threshold=dict(
                    type="int"
                ),
                turn_on_qos_logging=dict(type="bool"),
                update_account_log_every=dict(type="int"),
            ),
        ),
        one_time_password=dict(type="str", no_log=True),
        os_name=dict(type="str"),
        save_logs_locally=dict(type="bool"),
        send_alerts_to_server=dict(type="list", elements="str"),
        send_logs_to_backup_server=dict(type="list", elements="str"),
        send_logs_to_server=dict(type="list", elements="str"),
        tags=dict(type="list", elements="str"),
        threat_emulation=dict(type="bool"),
        threat_extraction=dict(type="bool"),
        url_filtering=dict(type="bool"),
        gateway_version=dict(type="str"),
        vpn=dict(type="bool"),
        vpn_settings=dict(
            type="dict",
            options=dict(
                maximum_concurrent_ike_negotiations=dict(type="int"),
                maximum_concurrent_tunnels=dict(type="int"),
            ),
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
        groups=dict(type="list", elements="str"),
        ignore_warnings=dict(type="bool"),
        ignore_errors=dict(type="bool"),
    )
    argument_spec.update(checkpoint_argument_spec_for_objects)

    module = AnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True
    )
    api_call_object = "simple-gateway"

    result = api_call(module, api_call_object)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
