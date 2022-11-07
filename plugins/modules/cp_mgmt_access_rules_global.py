#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for cp_mgmt_access_rules_global
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: cp_mgmt_access_rules_global
short_description: Manages ACCESS RULES resource module
description: ''
version_added: 3.3.0
options:
  config:
    description: A dictionary of ACCESS RULES options
    type: list
    elements: dict
    suboptions:
      layer:
        description: Layer that the rule belongs to identified by the name or UID.
        type: str
      position:
        description: Position in the rulebase.
        type: int
      name:
        description: Rule name.
        type: str
      action:
        description: '"Accept", "Drop", "Ask", "Inform", "Reject", "User Auth", "Client
          Auth", "Apply Layer".'
        type: str
      action_settings:
        description: Action settings.
        type: dict
        suboptions:
          enable_identity_captive_portal:
            description: N/A
            type: bool
          limit:
            description: N/A
            type: str
      content:
        description: List of processed file types that this rule applies on.
        type: list
        elements: str
      content_direction:
        description: On which direction the file types processing is applied.
        type: str
        choices:
        - any
        - up
        - down
      content_negate:
        description: True if negate is set for data.
        type: bool
      custom_fields:
        description: Custom fields.
        type: dict
        suboptions:
          field_1:
            description: First custom field.
            type: str
          field_2:
            description: Second custom field.
            type: str
          field_3:
            description: Third custom field.
            type: str
      destination:
        description: Collection of Network objects identified by the name or UID.
        type: list
        elements: str
      destination_negate:
        description: True if negate is set for destination.
        type: bool
      enabled:
        description: Enable/Disable the rule.
        type: bool
      inline_layer:
        description: Inline Layer identified by the name or UID. Relevant only if
          "Action" was set to "Apply Layer".
        type: str
      install_on:
        description: Which Gateways identified by the name or UID to install the policy
          on.
        type: list
        elements: str
      service:
        description: Collection of Network objects identified by the name or UID.
        type: list
        elements: str
      service_negate:
        description: True if negate is set for service.
        type: bool
      service_resource:
        description: Resource of the service identified by the name or UID. When a
          service-resource exists, the service parameter should contains exactly one
          service element.
        type: str
      source:
        description: Collection of Network objects identified by the name or UID.
        type: list
        elements: str
      source_negate:
        description: True if negate is set for source.
        type: bool
      time:
        description: 'List of time objects. For example: "Weekend", "Off-Work", "Every-Day".'
        type: list
        elements: str
      track:
        description: Track Settings.
        type: dict
        suboptions:
          accounting:
            description: Turns accounting for track on and off.
            type: bool
          alert:
            description: Type of alert for the track.
            type: str
            choices:
            - none
            - alert
            - snmp
            - mail
            - user alert 1
            - user alert 2
            - user alert 3
          enable_firewall_session:
            description: Determine whether to generate session log to firewall only
              connections.
            type: bool
          per_connection:
            description: Determines whether to perform the log per connection.
            type: bool
          per_session:
            description: Determines whether to perform the log per session.
            type: bool
          type:
            description: '"Log", "Extended Log", "Detailed  Log", "None".'
            type: str
      user_check:
        description: UserCheck settings.
        type: dict
        suboptions:
          confirm:
            description: N/A
            type: str
            choices:
            - per rule
            - per category
            - per application/site
            - per data type
          custom_frequency:
            description: N/A
            type: dict
            suboptions:
              every:
                description: N/A
                type: integer
              unit:
                description: N/A
                type: string
                choices:
                - hours
                - days
                - weeks
                - months
          frequency:
            description: N/A
            type: str
            choices:
            - once a day
            - once a week
            - once a month
            - custom frequency...
          interaction:
            description: N/A
            type: str
      vpn:
        description: Communities or Directional.
        type: dict
        suboptions:
          community:
            description: List of community name or UID.
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
      ignore_warnings:
        description: Apply changes ignoring warnings.
        type: bool
      ignore_errors:
        description: Apply changes ignoring errors. You won't be able to publish such
          a changes. If ignore-warnings flag was omitted - warnings will also be ignored.
        type: bool
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
author: Ansible Security Automation Team (@justjais) <https://github.com/ansible-security>
"""

EXAMPLES = """

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
  type: list
  sample: >
    This output will always be in the same format as the
    module argspec.
"""
