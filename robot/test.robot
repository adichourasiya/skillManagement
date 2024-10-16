*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${BASE_URL}      http://127.0.0.1:5000
${ADMIN_USER}    admin
${ADMIN_PASS}    admin_password
${STUDENT_USER}  student
${STUDENT_PASS}   student_password

*** Test Cases ***
Admin Can Log In And Manage Students
    [Documentation]    Verify admin can log in and manage students
    Open Browser    ${BASE_URL}    Chrome
    Maximize Browser Window
    Input Text    id=username    ${ADMIN_USER}
    Input Text    id=password    ${ADMIN_PASS}
    Click Button    id=login_button
    Wait Until Page Contains Element    id=student_name
    Close Browser

Student Can Log In And View Skills
    [Documentation]    Verify student can log in and view their skills
    Open Browser    ${BASE_URL}    Chrome
    Maximize Browser Window
    Input Text    id=username    ${STUDENT_USER}
    Input Text    id=password    ${STUDENT_PASS}
    Click Button    id=login_button
    Wait Until Page Contains Element    id=skills_table
    ${skills_count}    Get Element Count    id=skills_table tbody tr
    Should Be Greater Than    ${skills_count}    0
    Close Browser