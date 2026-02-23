*** Settings ***
Resource          resources/common.resource
Suite Setup       Create API Session

*** Keywords ***
Generate Unique Email
    [Arguments]    ${prefix}
    ${uuid}=    Evaluate    __import__('uuid').uuid4().hex[:8]
    RETURN    ${prefix}_${uuid}@example.com

*** Test Cases ***

# -------------------------------------------------------
# CREATE CLIENT
# -------------------------------------------------------

Create Client Successfully
    [Documentation]    Happy path: valid client should be created and return id and active status.
    ${response}=    Create Client    name=Acme Corp    email=acme_robot@example.com
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Be Equal    ${data}[name]    Acme Corp
    Should Be Equal    ${data}[email]    acme_robot@example.com
    Should Be Equal    ${data}[status]    active
    Dictionary Should Contain Key    ${data}    id

Create Client With All Fields
    [Documentation]    Client created with all optional fields should return them in response.
    ${response}=    Create Client
    ...    name=Full Client
    ...    email=full_robot@example.com
    ...    phone=+358401234567
    ...    business_id=1234567-8
    ...    note=VIP customer
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Be Equal    ${data}[phone]    +358401234567
    Should Be Equal    ${data}[business_id]    1234567-8

Create Client With Duplicate Email
    [Documentation]    Creating two clients with the same email should return 422 'Database does not accept the content'.
    Create Client    name=First Client    email=duplicate_robot@example.com
    ${response}=    Create Client    name=Second Client    email=duplicate_robot@example.com
    Should Be Equal As Integers    ${response.status_code}    422
    

Create Client Missing Email
    [Documentation]    Missing required email field should return 422 'Database does not accept the content'.
    ${body}=    Create Dictionary    name=No Email Client
    ${response}=    POST On Session    ${SESSION}    /clients/    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    422

Create Client Missing Name
    [Documentation]    Missing required name field should return 422 'Database does not accept the content'.
    ${body}=    Create Dictionary    email=noname_robot@example.com
    ${response}=    POST On Session    ${SESSION}    /clients/    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    422

# -------------------------------------------------------
# GET CLIENT
# -------------------------------------------------------

Get All Clients Returns List
    [Documentation]    After creating a client, GET /clients/ should return a non-empty list.
    Create Client    name=List Client    email=list_robot@example.com
    ${response}=    Get All Clients
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Not Be Empty    ${data}

Get Client By Valid ID
    [Documentation]    Should return the correct client when given a valid ID.
    ${create}=    Create Client    name=Findable Client    email=find_robot@example.com
    ${client_id}=    Set Variable    ${create.json()}[id]
    ${response}=    Get Client By ID    ${client_id}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[email]    find_robot@example.com

Get Client By Invalid ID
    [Documentation]    Non-existent client ID should return 404.
    ${response}=    Get Client By ID    99999
    Should Be Equal As Integers    ${response.status_code}    404
    Should Contain    ${response.json()}[detail]    not found

# -------------------------------------------------------
# UPDATE CLIENT
# -------------------------------------------------------

Update Client Name
    [Documentation]    PUT should update name while leaving other fields unchanged.
    ${create}=    Create Client    name=Old Name    email=update_robot@example.com
    ${client_id}=    Set Variable    ${create.json()}[id]
    ${body}=    Create Dictionary    name=New Name
    ${response}=    PUT On Session    ${SESSION}    /clients/${client_id}    json=${body}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[name]    New Name
    Should Be Equal    ${response.json()}[email]    update_robot@example.com

Update Client Not Found
    [Documentation]    PUT on non-existent client should return 404.
    ${body}=    Create Dictionary    name=Ghost
    ${response}=    PUT On Session    ${SESSION}    /clients/99999    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    404

Deactivate Client
    [Documentation]    PATCH should set client status to inactive.
    ${create}=    Create Client    name=Active Client    email=deactivate_robot@example.com
    ${client_id}=    Set Variable    ${create.json()}[id]
    ${response}=    PATCH On Session    ${SESSION}    /clients/${client_id}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[status]    inactive

Deactivate Client Not Found
    [Documentation]    PATCH on non-existent client should return 404.
    ${response}=    PATCH On Session    ${SESSION}    /clients/99999    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    404