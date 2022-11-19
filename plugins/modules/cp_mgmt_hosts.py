#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for cp_mgmt_hosts
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: cp_mgmt_hosts
short_description: Manages HOSTS resource module
description:
  - This resource module allows for addition, deletion, or modification of CP MGMT Hosts.
  - This resource module also takes care of gathering Hosts config facts
version_added: 4.1.0
options:
  config:
    description: A dictionary of HOSTS options
    type: dict
    suboptions:
      name:
        description: Object name. Must be unique in the domain.
        type: str
      ip_address:
        description: IPv4 or IPv6 address. If both addresses are required use ipv4-address
          and ipv6-address fields explicitly.
        type: str
      interfaces:
        description: Host interfaces.
        type: list
        elements: dict
        suboptions:
          name:
            description:
              - Interface name.
            type: str
          subnet:
            description:
              - IPv4 or IPv6 network address.
              - If both addresses are required use subnet4 and subnet6 fields explicitly.
            type: str
          subnet4:
            description:
              - IPv4 network address.
            type: str
          subnet6:
            description:
              - IPv6 network address.
            type: str
          mask_length:
            description:
              - IPv4 or IPv6 network mask length. If both masks are required use mask-length4 and
                mask-length6 fields explicitly.
              - Instead of IPv4 mask length it is possible to specify IPv4 mask itself in subnet-mask field.
            type: int
          mask_length4:
            description:
              - IPv4 network mask length.
            type: int
          mask_length6:
            description:
              - IPv6 network mask length.
            type: int
          subnet_mask:
            description:
              - IPv4 network mask.
            type: str
          color:
            description:
              - Color of the object. Should be one of existing colors.
            type: str
            choices:
              - 'aquamarine'
              - 'black'
              - 'blue'
              - 'crete blue'
              - 'burlywood'
              - 'cyan'
              - 'dark green'
              - 'khaki'
              - 'orchid'
              - 'dark orange'
              - 'dark sea green'
              - 'pink'
              - 'turquoise'
              - 'dark blue'
              - 'firebrick'
              - 'brown'
              - 'forest green'
              - 'gold'
              - 'dark gold'
              - 'gray'
              - 'dark gray'
              - 'light green'
              - 'lemon chiffon'
              - 'coral'
              - 'sea green'
              - 'sky blue'
              - 'magenta'
              - 'purple'
              - 'slate blue'
              - 'violet red'
              - 'navy blue'
              - 'olive'
              - 'orange'
              - 'red'
              - 'sienna'
              - 'yellow'
          comments:
            description:
              - Comments string.
            type: str
          details_level:
            description:
              - The level of detail for some of the fields in the response can vary from showing
                only the UID value of the object to a fully detailed representation of the object.
            type: str
            choices:
              - 'uid'
              - 'standard'
              - 'full'
          ignore_warnings:
            description:
              - Apply changes ignoring warnings.
            type: bool
          ignore_errors:
            description:
              - Apply changes ignoring errors. You won't be able to publish such a changes.
              - If ignore-warnings flag was omitted - warnings will also be ignored.
            type: bool
      nat_settings:
        description: NAT settings.
        type: dict
        suboptions:
          auto_rule:
            description:
              - Whether to add automatic address translation rules.
            type: bool
          ip_address:
            description:
              - IPv4 or IPv6 address. If both addresses are required use ipv4-address and ipv6-address fields explicitly.
              - This parameter is not required in case "method" parameter is "hide" and "hide-behind" parameter is "gateway".
            type: str
          ipv4_address:
            description:
              - IPv4 address.
            type: str
          ipv6_address:
            description:
              - IPv6 address.
            type: str
          hide_behind:
            description:
              - Hide behind method. This parameter is not required in case "method" parameter is "static".
            type: str
            choices:
              - 'gateway'
              - 'ip-address'
          install_on:
            description:
              - Which gateway should apply the NAT translation.
            type: str
          method:
            description:
              - NAT translation method.
            type: str
            choices:
              - 'hide'
              - 'static'
      tags:
        description: Collection of tag identifiers.
        type: list
        elements: str
      host_servers:
        description: Servers Configuration.
        type: dict
        suboptions:
          dns_server:
            description: Gets True if this server is a DNS Server.
            type: bool
          mail_server:
            description: Gets True if this server is a Mail Server.
            type: bool
          web_server:
            description: Gets True if this server is a Web Server.
            type: bool
          web_server_config:
            description: Web Server configuration.
            type: dict
            suboptions:
              additional_ports:
                description:
                  - Server additional ports.
                type: list
                elements: str
              application_engines:
                description:
                  - Application engines of this web server.
                type: list
                elements: str
              listen_standard_port:
                description:
                  - Whether server listens to standard port.
                type: bool
              operating_system:
                description:
                  - Operating System.
                type: str
                choices:
                  - 'sparc linux'
                  - 'windows'
                  - 'other'
                  - 'x86 linux'
                  - 'sparc solaris'
              protected_by:
                description:
                  - Network object which protects this server identified by the name or UID.
                type: str
      set_if_exists:
        description: If another object with the same identifier already exists, it
          will be updated. The command behaviour will be the same as if originally
          a set command was called. Pay attention that original object's fields will
          be overwritten by the fields provided in the request payload!
        type: bool
      color:
        description: Color of the object. Should be one of existing colors.
        type: str
        choices:
        - aquamarine
        - black
        - blue
        - crete blue
        - burlywood
        - cyan
        - dark green
        - khaki
        - orchid
        - dark orange
        - dark sea green
        - pink
        - turquoise
        - dark blue
        - firebrick
        - brown
        - forest green
        - gold
        - dark gold
        - gray
        - dark gray
        - light green
        - lemon chiffon
        - coral
        - sea green
        - sky blue
        - magenta
        - purple
        - slate blue
        - violet red
        - navy blue
        - olive
        - orange
        - red
        - sienna
        - yellow
      comments:
        description: Comments string.
        type: str
      details_level:
        description: The level of detail for some of the fields in the response can
          vary from showing only the UID value of the object to a fully detailed representation
          of the object.
        type: str
        choices:
        - uid
        - standard
        - full
      groups:
        description: Collection of group identifiers.
        type: list
        elements: str
      ignore_warnings:
        description: Apply changes ignoring warnings.
        type: bool
      ignore_errors:
        description: Apply changes ignoring errors. You won't be able to publish such
          a changes. If ignore-warnings flag was omitted - warnings will also be ignored.
        type: bool
      limit:
        description:
          - The maximal number of returned results.
          - NOTE, this parameter is a valid parameter only for the GATHERED state, for config states
            like, MERGED, REPLACED, and DELETED state it won't be applicable.
        type: int
      offset:
        description:
          - Number of the results to initially skip.
          - NOTE, this parameter is a valid parameter only for the GATHERED state, for config states
            like, MERGED, REPLACED, and DELETED state it won't be applicable.
        type: int
      order:
        description:
          - Sorts results by the given field. By default the results are sorted in the ascending order by name.
            This parameter is relevant only for getting few objects.
          - NOTE, this parameter is a valid parameter only for the GATHERED state, for config states
            like, MERGED, REPLACED, and DELETED state it won't be applicable.
        type: list
        elements: dict
        suboptions:
          ASC:
            description:
              - Sorts results by the given field in ascending order.
            type: str
          DESC:
            description:
              - Sorts results by the given field in descending order.
            type: str
      round_trip:
        description:
          - If set to True, the round trip will filter out the response param in the gathered result,
            and that will enable a user to fire the module config using the structured gathered data.
          - NOTE, this parameter makes sense only with the GATHERED state, as for config states like,
            MERGED, REPLACED, and DELETED state it won't be applicable as it's not a module config
            parameter.
        type: bool
      auto_publish_session:
        description:
          - Publish the current session if changes have been performed
            after task completes.
        type: bool
      version:
        description:
          - Version of checkpoint. If not given one, the latest version taken.
        type: str
  state:
    description:
    - The state the configuration should be left in
    - The state I(gathered) will get the module API configuration from the device
      and transform it into structured data in the format as per the module argspec
      and the value is returned in the I(gathered) key within the result.
    type: str
    choices:
    - merged
    - replaced
    - gathered
    - deleted
author: Ansible Team
"""

EXAMPLES = """

# Using MERGED state
# -------------------

- name: Merge MGMT Hosts config
  cp_mgmt_hosts:
    state: merged
    config:
      color: cyan
      ip_address: 192.0.2.1
      name: New Host 1
      auto_publish_session: true
      tags:
        - New Host

# RUN output:
# -----------

# mgmt_hosts:
#   after:
#     color: cyan
#     comments: ''
#     groups: []
#     icon: Objects/host
#     interfaces: []
#     ipv4-address: 192.0.2.1
#     name: New Host 1
#     nat_settings: {}
#     tags:
#     - New Host
#   before: {}

# Using REPLACED state
# --------------------

- name: Replace MGMT Host config
  cp_mgmt_hosts:
    state: replaced
    config:
      name: New Host 1
      tags:
        - New Replaced Host
      color: aquamarine
      ip_address: 198.51.110.0
      comments: REPLACED description
      ignore_warnings: true
      ignore_errors: false
      auto_publish_session: true

# RUN output:
# -----------

# mgmt_hosts:
#   after:
#     color: aquamarine
#     comments: REPLACED description
#     groups: []
#     icon: Objects/host
#     interfaces: []
#     ipv4-address: 198.51.110.0
#     name: New Host 1
#     nat_settings: {}
#     tags:
#     - New Replaced Host
#   before:
#     color: cyan
#     comments: ''
#     groups: []
#     icon: Objects/host
#     interfaces: []
#     ipv4-address: 192.0.2.1
#     name: New Host 1
#     nat_settings: {}
#     tags:
#     - New Host

# Using GATHERED state
# --------------------

# 1.
- name: Gather MGMT Host config by Name
  cp_mgmt_hosts:
    state: gathered
    config:
      name: New Host 1

# RUN output:
# -----------

# gathered:
#   color: cyan
#   comments: REPLACED description
#   domain: SMC User
#   groups: []
#   icon: Objects/host
#   interfaces: []
#   ipv4-address: 192.0.2.1
#   name: New Host 1
#   nat_settings: {}
#   read-only: false
#   tags:
#   - New Host
#   uid: 63b868bb-d300-47f4-b97a-c465a56fe9c7

# 2.

- name: Gather All hosts on the MGMT instance
  cp_mgmt_hosts:
    config:
      details_level: full
    state: gathered

# RUN output:
# -----------

# gathered:
#   - domain:
#       domain-type: domain
#       name: SMC User
#       uid: 41e821a0-3720-11e3-aa6e-0800200c9fde
#     ipv4-address: 172.17.178.237
#     name: asa-172.17.178.237
#     type: host
#     uid: d1f94d7d-fbba-4852-8827-2bdb6aabc9a5
#   - domain:
#       domain-type: domain
#       name: SMC User
#       uid: 41e821a0-3720-11e3-aa6e-0800200c9fde
#     ipv4-address: 192.0.2.1
#     name: New Host 1
#     type: host
#     uid: 63b868bb-d300-47f4-b97a-c465a56fe9c7

# Using DELETED state
# -------------------

- name: Delete MGMT Host config by Name
  cp_mgmt_hosts:
    state: deleted
    config:
      name: New Host 1

# RUN output:
# -----------

# mgmt_hosts:
#   after: {}
#   before:
#     color: cyan
#     comments: REPLACED description
#     groups: []
#     icon: Objects/host
#     interfaces: []
#     ipv4-address: 192.0.2.1
#     name: New Host 1
#     nat_settings: {}
#     tags:
#     - New Host

"""

RETURN = """
before:
  description: The configuration prior to the module execution.
  returned: when state is I(merged), I(replaced), I(deleted)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
after:
  description: The resulting configuration after module execution.
  returned: when changed
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
gathered:
  description: Facts about the network resource gathered from the remote device as structured data.
  returned: when state is I(gathered)
  type: dict
  sample: >
    This output will always be in the same format as the
    module argspec.
"""
