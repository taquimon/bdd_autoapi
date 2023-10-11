"""
(c) Copyright Jalasoft. 2023

steps_todo.py
    step definitions for feature files
"""
import json
import logging

from behave import given, when, then, step, use_step_matcher

from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)

# use_step_matcher("re")


@given('I set the base url and headers')
def step_set_base_url(context):
    LOGGER.debug("HEADERS: %s", context.headers)
    LOGGER.debug("URL: %s", context.url)
  

@then('I receive a {status_code:d} status code in response')
def step_verify_status_code(context, status_code):
    LOGGER.debug("Status code from response: %s", context.response["status"])
    LOGGER.debug("Status code param: %s", type(status_code))
    LOGGER.debug("Status code response: %s", type(context.response["status"]))
    assert int(status_code) == context.response["status"], " Expected 200 but received " + str(context.response["status"])


# @step(u'I call to projects endpoint using "(\\w*)" method( using the "([\\w\\s]*)" as parameter)*')
@step('I call to {feature} endpoint using "{method_name}" method using the "{param}" as parameter')
def step_when(context, feature, method_name, param):
    url = context.url + context.feature_name

    data = None
    if method_name == "POST":
        data = {
            "name": "Project 1"
        }
        if "update" in param:
            if feature == "projects":
                url = f"{url}/{context.project_id}"
        if context.text:
            LOGGER.debug("JSON: %s", context.text)
            context.dictionary = json.loads(context.text)
            context.dictionary["project_id"] = context.project_id
            data = context.dictionary

    if context.table:
        LOGGER.debug("Table: %s", context.table)
        index = 0
        for table in context.table:
            LOGGER.debug("row: %s", table[index])
            index += 1

    if method_name == "DELETE":
        feature_id = None
        if feature == "projects":
            feature_id = context.project_id
        elif feature == "sections":
            feature_id = context.section_id

        url = f"{context.url}{context.feature_name}/{feature_id}"
        
    response = RestClient().send_request(method_name=method_name.lower(), 
                                         session=context.session,
                                         url=url, 
                                         headers=context.headers,
                                         data=data)
    if method_name == "POST":
        if feature == "projects":
            context.project_list.append(response["body"]["id"])
        if feature == "sections":
            context.section_list.append(response["body"]["id"])
    
    context.response = response
    



