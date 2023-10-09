@projects @acceptance

Feature: Sections

  Scenario:  Verify GET all projects is returning all data correctly
      As a user I want to GET the projects from TODOIST API

    Given I set the base url and headers
    When I call to projects endpoint using "GET" method using the "None" as parameter
    Then I receive a 200 status code in response