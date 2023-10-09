import logging

from behave import given, when, then, step

from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


@given('I set the base url and headers')
def step_set_base_url(context):
    LOGGER.debug("HEADERS: %s", context.headers)
    LOGGER.debug("URL: %s", context.url)


@then('I receive a {status_code:d} status code in response')
def step_verify_status_code(context, status_code):
    LOGGER.debug("Status code from response: %s", context.response["status"])
    LOGGER.debug("Status code param: %s", type(status_code))
    LOGGER.debug("Status code response: %s", type(context.response["status"]))
    assert status_code == context.response["status"], " Expected 200 but recevied " + str(context.response["status"])

@step('I call to projects endpoint using "{method_name}" method using the "{param}" as parameter')
def step_when(context, method_name, param) :
    data = None
    if method_name == "POST":
        data = {
            "name" : "Project 1"
        }
    if context.table:
        LOGGER.debug("Table: %s", context.table)
        index = 0
        for table in context.table:
            LOGGER.debug("row: %s", table[index])
            index += 1
    url  = context.url

    if method_name == "DELETE":
        url = context.url + "/" + context.project_id
        
    response = RestClient().send_request(method_name=method_name.lower(), 
                                         session=context.session,
                                         url=url, 
                                         headers=context.headers,
                                         data=data)
    if method_name == "POST":
        context.project_list.append(response["body"]["id"])
    
    context.response = response
    



