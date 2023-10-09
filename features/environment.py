import logging
from urllib import response

import requests

from config.config import BASE_URL, HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


def before_all(context):    
    context.session = requests.Session()
    context.headers = HEADERS
    context.project_list = []
    context.url = BASE_URL
    LOGGER.debug("Headers before feature: %s", context.headers)


def before_feature(context, feature):
    context.feature_name = feature.name
    context.url = BASE_URL + feature.name.lower()
    print("Before feature")


def before_scenario(context, scenario):
  
    if "project_id" in scenario.tags:
        LOGGER.debug("Scenario tags: %s", scenario.tags)
        response = create_project(context=context, name_project="project x")        
        context.project_id = response["body"]["id"]
        LOGGER.debug("Project id created: %s", context.project_id)
        context.project_list.append(context.project_id)

def after_scenario(context, scenario):
    print("after scenario")


def after_feature(context, feature):
    print("After feature")


def after_all(context):
    print("After all")
    for project in context.project_list:
        url = f"{context.url}projects/{project}"
        RestClient().send_request(method_name="delete", session=context.session, 
                                  url=url, headers=HEADERS)
        LOGGER.info("Deleting project: %s", project)


def create_project(context, name_project):

    body_project = {
        "name": name_project
    }
    response = RestClient().send_request(method_name="post", session=context.session, 
                                         url=context.url, headers=context.headers, 
                                         data=body_project)
    
    return response
