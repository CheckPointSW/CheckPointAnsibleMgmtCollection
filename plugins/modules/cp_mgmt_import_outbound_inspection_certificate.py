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
module: cp_mgmt_import_outbound_inspection_certificate
short_description: Import Outbound Inspection certificate for HTTPS inspection.
description:
  - Import Outbound Inspection certificate for HTTPS inspection.
  - All operations are performed over Web Services API.
version_added: "3.0.0"
author: "Eden Brillant (@chkp-edenbr)"
options:
  base64_certificate:
    description:
      - Certificate file encoded in base64.<br/>Valid file format, p12.
    type: str
  base64_password:
    description:
      - Password (encoded in Base64 with padding) for the certificate file.
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
- name: import-outbound-inspection-certificate
  cp_mgmt_import_outbound_inspection_certificate:
    base64_certificate: MIIKSAIBAzCCCg4GCSqGSIb3DQEHAaCCCf8Eggn7MIIJ9zCCBI8GCSqGSIb3DQEHBqCCBIAwggR8AgEAMIIEdQYJKoZIhvc
                        NAQcBMBwGCiqGSIb3DQEMAQYwDgQILAfxjBi7DTQCAggAgIIESKgKoClNx4yTQr7xfIgSBSDs0It2vVsLubNFJpbQXzJUu2W
                        aPQPbqV3wISpWCa/auLYC9OWpTI89HFt30rVAdWCFVoty7jI6L8HjTYa8fTGyqW7PyfoGyZclmz6totsmeVWc8i7wnl9Hk8N
                        ZpLWuixNoSLQUqBoloyZEll3i3/Z+/6mDlYkRmpCMQA2YLQm1yc/3n7Fq6grBJDro0tIIoAwIzgCdoKqIMwlDNA9c0eaHeXs
                        P4k9WfJQbK6AyLTvHbrrNrgUyEDJQI6BCkeQwkBW2zRUHoe7s1DSQ5Rwft4koIaDcGovLES5g1gnXzmr4/23+rf4/EZszB0Q
                        vlYvZIKLQ8O2ofvZ/HK+59fxlhKEiEkW2yhezDGR9s6hZnzZ8vMutisQJ8MO0m9iKVD5AAtif/32iy5+TVIQfqgER+DYVGOu
                        k15YF2VcZGRlQ8pSvBXIkMMUDRqjFxQfKYIMlyk6RSSgmIn+EIA9GfaBmEGy2xJYvw6IkUJ+xoR+SYeLYiMw+HkzI+cCOKF7
                        fKPXlOCVvnESEeKwJ4inSxiI2GQG01aN/GNdsx/EM1Xi2LSHfzhG9URIOhjuJIQZn2Z7f3fpTxpWWCpEEVjcQZhoR0KX0DJ/
                        gIxiY8UsbNo58FTq5AwMFY6m8hxlHOorqh0MSE/x8LKq0v7JKIxQwrdkyUlVUqdaGreW5MgRdjqOrxQx53nLPdQelKWbR8Gn
                        4KkwFcYCAB1VAe944zqq6YKL4mvNwxk5wyqDjn5UZtPokKFfqBOwOSAGsaZ38x/2tqXEgPhWVGFPJlsIUUKBRVTtqxsb2Lda
                        CPHjO8bQhhgOIMEav+iWZAJYudZuolr8Aviccorg1w0sr2eklHbO6yMWrDrvlCVpSawRnLIeeWe+4rwV7SNdcA5hSombTWKR
                        cR8mOkTGjpByiz6+g+3mHOebyTrmIfUSENMZy5oYjQfDyNLi0RMmCPCqMjRSwyAs/CDhzz4wTFLEYbu+fUrm2WZc2vhhxafb
                        VrbZ+FcDcnYomYfp8aSxiIIq8+gxT99Oi3WNqhJ+IZGJODWMYRfpKNwgCab8uJt8TV3SVXVIXW0Y28l4ZP/qWEfnEC8Wl6HJ
                        GhJo7arqBFTWWEuKvHw985OpksavdQFXgVU9Egbue0anb0U5SDyRu0hqJ/Gw83dKJbCg8hPv4gGq/yeOb+cX63DCKvOcoXjZ
                        0szeRcGiro0+BSgr143Ks19lsxWHPOlauLSnD3jVrgpmVwxCizRTnX3OLJ07IpvvEJGAQR/Ru2lo7eN0H4933G93tVQtte69
                        BiPwbkWtSx8ddzbRGmMW7IsG72FVm5QrJC1C1Na5xqQQV6G2oHqIHNdNyXD6TmhuQ4BnpCoamCzfsX4iozS+NySz/Jdbuj0Y
                        Z9L2dYUHiBF4xotlHfwiAiCghaBH31OZJ0n52d0NGqRkN5F0Qdfz1O2+rLx2zswggVgBgkqhkiG9w0BBwGgggVRBIIFTTCCB
                        UkwggVFBgsqhkiG9w0BDAoBAqCCBO4wggTqMBwGCiqGSIb3DQEMAQMwDgQIRNvl6KdajoCAggABIIEyBJbsgafEO1D9xQ8BF
                        YFNKf/meJNAOO4XVPTFtUBpyvEn3PkyxyKU1cMenESXeMacSv/VftkYC7CwN81kzbRMRSEXZSCsyj48kMqwTqMNmZmgF8XaF
                        vzXOGlu2E411LZ/sOenWO7lxeNGZM3vk4FWvl+4fa5Xd5TDqya65VsXSocDUA5kpeqn323TcdeCldGmEniX85NGIiPpWuRLG
                        rNf8VOIuE3NFAmTSveHH9Oo7PjscCifc7O4+NpOW9GfayZMqG8dTpLhIRacdvy/QvbWePXdzzSI9rKogX/7bSzU0Hq+8rpWl
                        Ahz0qnW2Bb3T7of86Len5cuNr0k425Dhpuo4od81exDdSa3+aFQqR3nKVSkPapLBrpGNZIX4TwctRnbi2ZHdFxMKkJewGt/b
                        eam3LcujJRlN2RBeA0IRWEAyO6ubjpQ62ChrW+faHXXxYH3Be6nPXSF5pq4VAIVglNsPOxGYIb+qNDhOblzQBq4nF30fyHmO
                        wDIRgNWwOStT7dUFmN0ouHinP6QXWBDDQiDo2RRFs2/RWu0ZY0EAzEYAMCSvmk+SQgKbKpNFf0C5kuJ56PWXUuGSoAXV/vxv
                        K6OHIGFFcZo+VrRgYTHY/eSjw1+/lpUkwaWAzoH0X6KxuLXfgzv+E8Z+LFVWIAoknJ96ieljiHzNnfeSTZYwTaJbYaritdAQ
                        2MTGcBrpJFIqr9GjWGVsFQK0ct/ZIFzZw0Vnt/aOj5OjMPlpy9UXfC+tw9gfRYWfSuDLuUH0Znu3JB/+J2XQP4PBArXKyvFv
                        6wMVSvY/04r2WQQKV9YTUCkbgvHAlQ7vP0a8z44xSrKc4M04sEBE3cFD2NBAQrP3GqRyz2ukuzJhrj/B1dZWA23SZaqfN9gp
                        bfFbtPXN6F/nY1UUsikLjcXDjC8GVU9Pp4VCnv2EUgl4QmkUEdVeDZjUnz/k9Kd53q3h+chAId+3VBsemd3ZadX4gupw6Xf
                        6zT8Av7v75/1/vFw2yz22DG8pIpN4uuEdSFhvs9lr6f2M6bQABS+NWfehq5aqBqsXXX8R3fSxYLL0gO4lxf4YqSomA4AlzS9
                        tJtEe2DKWYmnYwiiUGYLs7aGMLZQbHbYutPKKZXTaSGWYBaIrVjbDM67la/csYmxpb2n6UD6TkNICuZwd/ImVvDhbCEsR/EU
                        +YU0HPwxlUtcCsqw4Vy8rBtbla2XmegGUcLWSurKmq42SW8WLBJQfY/9sWyaMqSGy0/Vq4/+/CtXUZ1N5rgibYyIZ9Tvm/nd
                        v2xBW1hYivIZZQFRbg5fWxKA5ifYejGmYCWGQynRSVCbqccw08xy5Iwnww4v5Cz5bcNyRLFOU2/bfn7SC5mcQ/Tw5ZKOQVRn
                        88G78amMPHRqX4RzPtIwmK+B3zPJX0MHrY3w5hzPZ0UCtR2YsbYLeqsYP6b+RBLSV3wtkUZ9PgbMeu7zXSE0z1svGpjF7yWp
                        nP47ilbxwe1YXL5+CuqN6iHFfyaP1JPYILmHdw0gzgyOdo1y4rUXgCeiCyH4vJVLts8EKpXZDMCUmujb306IOD9haFXdQHV5
                        XlQurtw+JC7ySe9bVMrzYJv5/oPioOXMnLPI2OXYbACwlQ/UHgl5LmDlsxeairdfYTdAxajFEMB0GCSqGSIb3DQEJFDEQHg4
                        AbQB5AGEAbABpAGEAczAjBgkqhkiG90BCRUxFgQU7cUIcmKuQKAMfwbKiKzQozUsyHwwMTAhMAkGBSsOAwIaBQAEFEFoI0QT
                        Iv2s2lR8PxS8xfiT5S06BAjANT3YLoakoAICCAA=
    base64_password: bXlfcGFzc3dvcmQ=
"""

RETURN = """
cp_mgmt_import_outbound_inspection_certificate:
  description: The checkpoint import-outbound-inspection-certificate output.
  returned: always.
  type: dict
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.check_point.mgmt.plugins.module_utils.checkpoint import checkpoint_argument_spec_for_commands, api_command


def main():
    argument_spec = dict(
        base64_certificate=dict(type='str'),
        base64_password=dict(type='str', no_log=True),
        details_level=dict(type='str', choices=['uid', 'standard', 'full']),
        auto_publish_session=dict(type='bool')
    )
    argument_spec.update(checkpoint_argument_spec_for_commands)

    module = AnsibleModule(argument_spec=argument_spec)

    command = "import-outbound-inspection-certificate"

    result = api_command(module, command)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
