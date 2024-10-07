*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${BASE_URL}      http://127.0.0.1:5000
${ADMIN_USER}    admin_username
${ADMIN_PASS}    admin_password
${STUDENT_USER}  student_username
${STUDENT_PASS}   student_password

*** Test Cases ***
Admin Can Log In And Manage Students
    [Documentation]    Verify admin can log in and manage students
    Open Browser    ${BASE_URL}    Chrome
    Maximize Browser Window
    Input Text    id=username    ${ADMIN_USER}
    Input Text    id=password    ${ADMIN_PASS}
    Click Button    id=login_button
    Wait Until Page Contains Element    id=students_table
    ${students_before}    Get Element Count    id=students_table tbody tr
    Input Text    id=student_name    New Student
    Click Button    id=add_student
    Wait Until Page Contains Element    id=students_table
    ${students_after}    Get Element Count    id=students_table tbody tr
    Should Be Equal    ${students_after}    ${students_before + 1}
    Click Button    id=remove_student    ${students_after - 1}
    Wait Until Page Contains Element    id=students_table
    ${students_final}    Get Element Count    id=students_table tbody tr
    Should Be Equal    ${students_final}    ${students_before}
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
