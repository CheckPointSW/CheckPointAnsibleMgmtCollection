# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2018 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import time

from ansible.module_utils.connection import Connection

checkpoint_argument_spec_for_action_module = dict(
    auto_publish_session=dict(type='bool'),
    wait_for_task_timeout=dict(type='int', default=30),
    version=dict(type='str')
)

checkpoint_argument_spec_for_objects = dict(
    auto_publish_session=dict(type='bool'),
    wait_for_task=dict(type='bool', default=True),
    wait_for_task_timeout=dict(type='int', default=30),
    state=dict(type='str', choices=['present', 'absent'], default='present'),
    version=dict(type='str')
)

checkpoint_argument_spec_for_facts = dict(
    version=dict(type='str')
)

checkpoint_argument_spec_for_commands = dict(
    wait_for_task=dict(type='bool', default=True),
    wait_for_task_timeout=dict(type='int', default=30),
    version=dict(type='str')
)

delete_params = ['name', 'uid', 'layer', 'exception-group-name', 'rule-name', 'package']

remove_from_set_payload = {'lsm-cluster': ['security-profile', 'name-prefix', 'name-suffix', 'main-ip-address'],
                           'md-permissions-profile': ['permission-level']}

remove_from_add_payload = {'lsm-cluster': ['name']}


# parse failure message with code and response
def parse_fail_message(code, response):
    return 'Checkpoint device returned error {0} with message {1}'.format(code, response)


# send the request to checkpoint
def send_request(connection, version, url, payload=None):
    code, response = connection.send_request('/web_api/' + version + url, payload)

    return code, response


# get the payload from the user parameters
def is_checkpoint_param(parameter):
    if parameter == 'auto_publish_session' or \
            parameter == 'state' or \
            parameter == 'wait_for_task' or \
            parameter == 'wait_for_task_timeout' or \
            parameter == 'version':
        return False
    return True


def contains_show_identifier_param(payload):
    identifier_params = ["name", "uid", "assigned-domain"]
    for param in identifier_params:
        if payload.get(param) is not None:
            return True
    return False


# build the payload from the parameters which has value (not None), and they are parameter of checkpoint API as well
def get_payload_from_parameters(params):
    payload = {}
    for parameter in params:
        parameter_value = params[parameter]
        if parameter_value is not None and is_checkpoint_param(parameter):
            if isinstance(parameter_value, dict):
                payload[parameter.replace("_", "-")] = get_payload_from_parameters(parameter_value)
            elif isinstance(parameter_value, list) and len(parameter_value) != 0 and isinstance(parameter_value[0], dict):
                payload_list = []
                for element_dict in parameter_value:
                    payload_list.append(get_payload_from_parameters(element_dict))
                payload[parameter.replace("_", "-")] = payload_list
            else:
                # special handle for this param in order to avoid two params called "version"
                if parameter == "gateway_version" or parameter == "cluster_version":
                    parameter = "version"

                payload[parameter.replace("_", "-")] = parameter_value

            # action module "access_rules" - convert position_by_rule to position
            if parameter == "position_by_rule":
                if 'below' in params['position_by_rule'].keys() and params['position_by_rule']['below']:
                    position = {'position': {'below': params['position_by_rule']['below']}}
                    payload.update(position)
                elif 'above' in params['position_by_rule'].keys() and params['position_by_rule']['above']:
                    position = {'position': {'above': params['position_by_rule']['above']}}
                    payload.update(position)
                del payload['position-by-rule']

    return payload


# wait for task
def wait_for_task(module, version, connection, task_id):
    task_id_payload = {'task-id': task_id, 'details-level': 'full'}
    task_complete = False
    minutes_until_timeout = 30
    if module.params['wait_for_task_timeout'] is not None and module.params['wait_for_task_timeout'] >= 0:
        minutes_until_timeout = module.params['wait_for_task_timeout']
    max_num_iterations = minutes_until_timeout * 30
    current_iteration = 0

    # As long as there is a task in progress
    while not task_complete and current_iteration < max_num_iterations:
        current_iteration += 1
        # Check the status of the task
        code, response = send_request(connection, version, 'show-task', task_id_payload)

        attempts_counter = 0
        while code != 200:
            if attempts_counter < 5:
                attempts_counter += 1
                time.sleep(2)
                code, response = send_request(connection, version, 'show-task', task_id_payload)
            else:
                response['message'] = "ERROR: Failed to handle asynchronous tasks as synchronous, tasks result is" \
                                      " undefined. " + response['message']
                module.fail_json(msg=parse_fail_message(code, response))

        # Count the number of tasks that are not in-progress
        completed_tasks = 0
        for task in response['tasks']:
            if task['status'] == 'failed':
                status_description, comments = get_status_description_and_comments(task)
                if comments and status_description:
                    module.fail_json(
                        msg='Task {0} with task id {1} failed. Message: {2} with description: {3} - '
                            'Look at the logs for more details '
                            .format(task['task-name'], task['task-id'], comments, status_description))
                elif comments:
                    module.fail_json(msg='Task {0} with task id {1} failed. Message: {2} - Look at the logs for more details '
                                         .format(task['task-name'], task['task-id'], comments))
                elif status_description:
                    module.fail_json(msg='Task {0} with task id {1} failed. Message: {2} - Look at the logs for more '
                                         'details '
                                     .format(task['task-name'], task['task-id'], status_description))
                else:
                    module.fail_json(msg='Task {0} with task id {1} failed. Look at the logs for more details'
                                     .format(task['task-name'], task['task-id']))
            if task['status'] == 'in progress':
                break
            completed_tasks += 1

        # Are we done? check if all tasks are completed
        if completed_tasks == len(response["tasks"]) and completed_tasks != 0:
            task_complete = True
        else:
            time.sleep(2)  # Wait for two seconds
    if not task_complete:
        module.fail_json(msg="ERROR: Timeout. Task-id: {0}.".format(task_id_payload['task-id']))
    else:
        return response


# Getting a status description and comments of task failure details
def get_status_description_and_comments(task):
    status_description = None
    comments = None
    if 'comments' in task and task['comments']:
        comments = task['comments']
    if 'task-details' in task and task['task-details']:
        task_details = task['task-details'][0]
        if 'statusDescription' in task_details:
            status_description = task_details['statusDescription']
    return status_description, comments


# if failed occurred, in some cases we want to discard changes before exiting. We also notify the user about the `discard`
def discard_and_fail(module, code, response, connection, version):
    discard_code, discard_response = send_request(connection, version, 'discard')
    if discard_code != 200:
        try:
            module.fail_json(msg=parse_fail_message(code, response) + ' Failed to discard session {0}'
                                                                      ' with error {1} with message {2}'.format(connection.get_session_uid(),
                                                                                                                discard_code, discard_response))
        except Exception:
            # Read-only mode without UID
            module.fail_json(msg=parse_fail_message(code, response) + ' Failed to discard session'
                                                                      ' with error {0} with message {1}'.format(discard_code, discard_response))

    module.fail_json(msg=parse_fail_message(code, response) + ' Unpublished changes were discarded')


# handle publish command, and wait for it to end if the user asked so
def handle_publish(module, connection, version):
    if 'auto_publish_session' in module.params and module.params['auto_publish_session']:
        publish_code, publish_response = send_request(connection, version, 'publish')
        if publish_code != 200:
            discard_and_fail(module, publish_code, publish_response, connection, version)
        if module.params['wait_for_task']:
            wait_for_task(module, version, connection, publish_response['task-id'])


# if user insert a specific version, we add it to the url
def get_version(module):
    return ('v' + module.params['version'] + '/') if module.params.get('version') else ''


# if code is 400 (bad request) or 500 (internal error) - fail
def handle_equals_failure(module, equals_code, equals_response):
    if equals_code == 400 or equals_code == 500:
        module.fail_json(msg=parse_fail_message(equals_code, equals_response))
    if equals_code == 404 and equals_response['code'] == 'generic_err_command_not_found':
        module.fail_json(msg='Relevant hotfix is not installed on Check Point server. See sk114661 on Check Point Support Center.')


# handle call
def handle_call(connection, version, call, payload, module, to_publish, to_discard_on_failure):
    code, response = send_request(connection, version, call, payload)
    if code != 200:
        if to_discard_on_failure:
            discard_and_fail(module, code, response, connection, version)
        else:
            module.fail_json(msg=parse_fail_message(code, response))
    else:
        if 'wait_for_task' in module.params and module.params['wait_for_task']:
            if 'task-id' in response:
                response = wait_for_task(module, version, connection, response['task-id'])
            elif 'tasks' in response:
                for task in response['tasks']:
                    if 'task-id' in task:
                        task_id = task['task-id']
                        response[task_id] = wait_for_task(module, version, connection, task['task-id'])
                del response['tasks']
    if to_publish:
        handle_publish(module, connection, version)
    return response


# handle a command
def api_command(module, command):
    payload = get_payload_from_parameters(module.params)
    connection = Connection(module._socket_path)
    version = get_version(module)

    code, response = send_request(connection, version, command, payload)
    result = {'changed': True}

    if code == 200:
        if module.params['wait_for_task']:
            if 'task-id' in response:
                response = wait_for_task(module, version, connection, response['task-id'])
            elif 'tasks' in response:
                for task in response['tasks']:
                    if 'task-id' in task:
                        task_id = task['task-id']
                        response[task_id] = wait_for_task(module, version, connection, task['task-id'])
                del response['tasks']

        result[command] = response

        handle_publish(module, connection, version)
    else:
        discard_and_fail(module, code, response, connection, version)

    return result


# handle api call facts
def api_call_facts(module, api_call_object, api_call_object_plural_version):
    payload = get_payload_from_parameters(module.params)
    connection = Connection(module._socket_path)
    version = get_version(module)

    # if there isn't an identifier param, the API command will be in plural version (e.g. show-hosts instead of show-host)
    if not contains_show_identifier_param(payload):
        api_call_object = api_call_object_plural_version

    response = handle_call(connection, version, 'show-' + api_call_object, payload, module, False, False)
    result = {api_call_object: response}
    return result


# handle delete
def handle_delete(equals_code, payload, delete_params, connection, version, api_call_object, module, result):
    # else equals_code is 404 and no need to delete because he doesn't exist
    if equals_code == 200:
        payload_for_delete = extract_payload_with_some_params(payload, delete_params)
        response = handle_call(connection, version, 'delete-' + api_call_object, payload_for_delete, module, True, True)
        result['changed'] = True


# handle the call and set the result with 'changed' and teh response
def handle_call_and_set_result(connection, version, call, payload, module, result):
    response = handle_call(connection, version, call, payload, module, True, True)
    result['changed'] = True
    result[call] = response


# handle api call
def api_call(module, api_call_object):
    payload = get_payload_from_parameters(module.params)
    connection = Connection(module._socket_path)
    version = get_version(module)

    result = {'changed': False}
    if module.check_mode:
        return result

    payload_for_equals = {'type': api_call_object, 'params': payload}
    equals_code, equals_response = send_request(connection, version, 'equals', payload_for_equals)
    result['checkpoint_session_uid'] = connection.get_session_uid()
    handle_equals_failure(module, equals_code, equals_response)

    if module.params['state'] == 'present':
        if equals_code == 200:
            # else objects are equals and there is no need for set request
            if not equals_response['equals']:
                build_payload(api_call_object, payload, remove_from_set_payload)
                handle_call_and_set_result(connection, version, 'set-' + api_call_object, payload, module, result)
        elif equals_code == 404:
            build_payload(api_call_object, payload, remove_from_add_payload)
            handle_call_and_set_result(connection, version, 'add-' + api_call_object, payload, module, result)
    elif module.params['state'] == 'absent':
        handle_delete(equals_code, payload, delete_params, connection, version, api_call_object, module, result)

    return result


# get the position in integer format
def get_number_from_position(payload, connection, version, show_rulebase_command):
    if type(payload['position']) is not dict:
        position = payload['position']
        if position == 'top':
            position = 1
        elif position == 'bottom':
            payload_for_show_obj_rulebase = {'name': payload['layer'], 'limit': 0}
            code, response = send_request(connection, version, show_rulebase_command, payload_for_show_obj_rulebase)
            position = response['total']
    else:
        position = None
        payload_for_show_access_rulebase = {'name': payload['layer']}
        code, response = send_request(connection, version, 'show-access-rulebase', payload_for_show_access_rulebase)
        rulebase = response['rulebase']
        for rules in rulebase:
            if 'rulebase' in rules:
                rules = rules['rulebase']
                for rule in rules:
                    if 'below' in payload['position'].keys() and rule['name'] == payload['position']['below']:
                        position = int(rule['rule-number']) + 1
                        return position
                    elif 'above' in payload['position'].keys() and rule['name'] == payload['position']['above']:
                        position = max(int(rule['rule-number']) - 1, 1)
                        return position
            elif 'below' in payload['position'].keys() and rules['name'] == payload['position']['below']:
                position = int(rules['rule-number']) + 1
                return position
            elif 'above' in payload['position'].keys() and rules['name'] == payload['position']['above']:
                position = max(int(rules['rule-number']) - 1, 1)
                return position
        return position

    return int(position)


# build the show rulebase payload
def build_rulebase_payload(api_call_object, payload, position_number):
    rulebase_payload = {'name': payload['layer'], 'offset': position_number - 1, 'limit': 1}

    if api_call_object == 'threat-exception':
        rulebase_payload['rule-name'] = payload['rule-name']

    return rulebase_payload


def build_rulebase_command(api_call_object):
    rulebase_command = 'show-' + api_call_object.split('-')[0] + '-rulebase'

    if api_call_object == 'threat-exception':
        rulebase_command = 'show-threat-rule-exception-rulebase'

    return rulebase_command


# remove from payload unrecognized params (used for cases where add payload differs from that of a set)
def build_payload(api_call_object, payload, params_to_remove):
    if api_call_object in params_to_remove:
        for param in params_to_remove[api_call_object]:
            del payload[param]
    return payload


# extract rule from rulebase response
def extract_rule_from_rulebase_response(response):
    rule = response['rulebase'][0]
    while 'rulebase' in rule:
        rule = rule['rulebase'][0]
    return rule


def get_relevant_show_rulebase_command(api_call_object):
    if api_call_object == 'access-rule':
        return 'show-access-rulebase'
    elif api_call_object == "threat-rule":
        return 'show-threat-rulebase'
    elif api_call_object == "threat-exception":
        return 'show-threat-rule-exception-rulebase'
# uncomment code below when https & nat modules are added as crud modules
    # elif api_call_object == 'nat-rule':
    #     return 'show-nat-rulebase'
    # elif api_call_object == 'https-rule':
    #     return 'show-https-rulebase'


# is the param position (if the user inserted it) equals between the object and the user input
def is_equals_with_position_param(payload, connection, version, api_call_object):
    # if there is no position param, then it's equals in vacuous truth
    if 'position' not in payload:
        return True

    position_number = payload['position']

    rulebase_payload = build_rulebase_payload(api_call_object, payload, position_number)
    rulebase_command = build_rulebase_command(api_call_object)

    code, response = send_request(connection, version, rulebase_command, rulebase_payload)

    # if true, it means there is no rule in the position that the user inserted, so I return false, and when we will try to set
    # the rule, the API server will get throw relevant error
    if response['total'] < position_number:
        return False

    rule = extract_rule_from_rulebase_response(response)

    # if the names of the exist rule and the user input rule are equals, then it's means that their positions are equals so I
    # return True. and there is no way that there is another rule with this name cause otherwise the 'equals' command would fail
    if rule['name'] == payload['name']:
        return True
    else:
        return False


# get copy of the payload without some of the params
def extract_payload_without_some_params(payload, params_to_remove):
    copy_payload = dict(payload)
    for param in params_to_remove:
        if param in copy_payload:
            del copy_payload[param]
    return copy_payload


# get copy of the payload with only some of the params
def extract_payload_with_some_params(payload, params_to_insert):
    copy_payload = {}
    for param in params_to_insert:
        if param in payload:
            copy_payload[param] = payload[param]
    return copy_payload


# is equals with all the params including action and position
def is_equals_with_all_params(payload, connection, version, api_call_object, is_access_rule):
    if is_access_rule and 'action' in payload:
        payload_for_show = extract_payload_with_some_params(payload, ['name', 'uid', 'layer'])
        code, response = send_request(connection, version, 'show-' + api_call_object, payload_for_show)
        exist_action = response['action']['name']
        if exist_action.lower() != payload['action'].lower():
            if payload['action'].lower() != 'Apply Layer'.lower() or\
                    exist_action.lower() != 'Inner Layer'.lower():
                return False

    # here the action is equals, so check the position param
    if not is_equals_with_position_param(payload, connection, version, api_call_object):
        return False

    return True


# handle api call for rule
def api_call_for_rule(module, api_call_object):
    is_access_rule = True if 'access' in api_call_object else False
    payload = get_payload_from_parameters(module.params)
    connection = Connection(module._socket_path)
    version = get_version(module)

    result = {'changed': False}
    if module.check_mode:
        return result

    if is_access_rule:
        copy_payload_without_some_params = extract_payload_without_some_params(payload, ['action', 'position'])
    else:
        copy_payload_without_some_params = extract_payload_without_some_params(payload, ['position'])
    payload_for_equals = {'type': api_call_object, 'params': copy_payload_without_some_params}
    equals_code, equals_response = send_request(connection, version, 'equals', payload_for_equals)
    result['checkpoint_session_uid'] = connection.get_session_uid()
    handle_equals_failure(module, equals_code, equals_response)

    if module.params['state'] == 'present':
        if equals_code == 200:
            if 'position' in payload:
                payload['position'] = get_number_from_position(payload, connection, version,
                                                               get_relevant_show_rulebase_command(api_call_object))
            if equals_response['equals']:
                if not is_equals_with_all_params(payload, connection, version, api_call_object, is_access_rule):
                    equals_response['equals'] = False
            # else objects are equals and there is no need for set request
            if not equals_response['equals']:
                # if user insert param 'position' and needed to use the 'set' command, change the param name to 'new-position'
                if 'position' in payload:
                    payload['new-position'] = payload['position']
                    del payload['position']
                handle_call_and_set_result(connection, version, 'set-' + api_call_object, payload, module, result)
        elif equals_code == 404:
            handle_call_and_set_result(connection, version, 'add-' + api_call_object, payload, module, result)
    elif module.params['state'] == 'absent':
        handle_delete(equals_code, payload, delete_params, connection, version, api_call_object, module, result)

    return result


# check if call is in plural form
def call_is_plural(api_call_object, payload):
    is_plural = False
    if 'access' in api_call_object and payload.get("layer") is None:
        is_plural = True
    elif 'threat' in api_call_object and payload.get("layer") is None:
        is_plural = True
    elif 'nat' in api_call_object \
            and payload.get("name") is None \
            and payload.get("uid") is None \
            and payload.get("rule-number") is None:
        is_plural = True
    return is_plural


# handle api call facts for rule
def api_call_facts_for_rule(module, api_call_object, api_call_object_plural_version):
    payload = get_payload_from_parameters(module.params)
    connection = Connection(module._socket_path)
    version = get_version(module)

    # if there is no layer, the API command will be in plural version (e.g. show-hosts instead of show-host)
    if call_is_plural(api_call_object, payload):
        api_call_object = api_call_object_plural_version

    response = handle_call(connection, version, 'show-' + api_call_object, payload, module, False, False)
    result = {api_call_object: response}
    return result


# The code from here till EOF will be deprecated when Rikis' modules will be deprecated
checkpoint_argument_spec = dict(auto_publish_session=dict(type='bool', default=True),
                                policy_package=dict(type='str', default='standard'),
                                auto_install_policy=dict(type='bool', default=True),
                                targets=dict(type='list')
                                )


def publish(connection, uid=None):
    payload = None

    if uid:
        payload = {'uid': uid}

    connection.send_request('/web_api/publish', payload)


def discard(connection, uid=None):
    payload = None

    if uid:
        payload = {'uid': uid}

    connection.send_request('/web_api/discard', payload)


def install_policy(connection, policy_package, targets):
    payload = {'policy-package': policy_package,
               'targets': targets}

    connection.send_request('/web_api/install-policy', payload)


def prepare_rule_params_for_execute_module(rule, module_args, position, below_rule_name):
    rule['layer'] = module_args['layer']
    if 'details_level' in module_args.keys():
        rule['details_level'] = module_args['details_level']
    if 'state' not in rule.keys() or ('state' in rule.keys() and rule['state'] != 'absent'):
        if below_rule_name:
            position_by_rule = {'position_by_rule': {'below': below_rule_name}}
            rule.update(position_by_rule)
        else:
            rule['position'] = position
        position = position + 1
        below_rule_name = rule['name']

    return rule, position, below_rule_name


def check_if_to_publish_for_action(result, module_args):
    to_publish = ('auto_publish_session' in module_args.keys() and module_args['auto_publish_session']) and \
                 ('changed' in result.keys() and result['changed'] is True) and ('failed' not in result.keys() or
                                                                                 result['failed'] is False)
    return to_publish
