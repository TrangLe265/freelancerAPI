*** Settings ***
Resource          resources/common.resource
Suite Setup       Create API Session

*** Keywords ***
Create Test Client
    ${uuid}=    Evaluate    __import__('uuid').uuid4().hex[:8]
    ${email}=    Set Variable    gigtest_${uuid}@example.com
    ${response}=    Create Client    name=Gig Test Client    email=${email}
    Should Be Equal As Integers    ${response.status_code}    200
    RETURN    ${response.json()}[id]

*** Test Cases ***

# -------------------------------------------------------
# CREATE GIG
# -------------------------------------------------------

Create Gig Successfully
    [Documentation]    Happy path: valid gig linked to existing client.
    ${client_id}=    Create Test Client
    ${response}=    Create Gig
    ...    client_id=${client_id}
    ...    title=Logo Design
    ...    wage=${800}
    ...    date=2026-04-01
    ...    location=Remote
    ...    description=Brand logo package
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Be Equal    ${data}[title]    Logo Design
    Should Be Equal As Numbers    ${data}[wage]    800
    Should Be Equal    ${data}[status]    pending

Create Gig Missing Wage
    [Documentation]    Wage is required — missing it should return 422.
    ${client_id}=    Create Test Client
    ${body}=    Create Dictionary    client_id=${client_id}    title=No Wage    date=2026-04-01
    ${response}=    POST On Session    ${SESSION}    /gigs/    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    422

Create Gig Missing Date
    [Documentation]    Date is required — missing it should return 422.
    ${client_id}=    Create Test Client
    ${body}=    Create Dictionary    client_id=${client_id}    title=No Date    wage=${500}
    ${response}=    POST On Session    ${SESSION}    /gigs/    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    422

# -------------------------------------------------------
# GET GIG
# -------------------------------------------------------

Get Gig By Valid ID
    [Documentation]    Should return the correct gig when given a valid ID.
    ${client_id}=    Create Test Client
    ${create}=    Create Gig    client_id=${client_id}    title=Findable Gig    wage=${600}    date=2026-04-01
    ${gig_id}=    Set Variable    ${create.json()}[id]
    ${response}=    Get Gig By ID    ${gig_id}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[title]    Findable Gig

Get Gig By Invalid ID
    [Documentation]    Non-existent gig ID should return 404.
    ${response}=    Get Gig By ID    99999
    Should Be Equal As Integers    ${response.status_code}    404

# -------------------------------------------------------
# UPDATE GIG
# -------------------------------------------------------

Update Gig Wage
    [Documentation]    Should update wage and return updated gig.
    ${client_id}=    Create Test Client
    ${create}=    Create Gig    client_id=${client_id}    title=Update Wage Gig    wage=${500}    date=2026-04-01
    ${gig_id}=    Set Variable    ${create.json()}[id]
    ${body}=    Create Dictionary    wage=${1200}
    ${response}=    PUT On Session    ${SESSION}    /gigs/${gig_id}    json=${body}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal As Numbers    ${response.json()}[wage]    1200

Update Gig Title
    [Documentation]    Should update title without affecting wage.
    ${client_id}=    Create Test Client
    ${create}=    Create Gig    client_id=${client_id}    title=Old Title    wage=${700}    date=2026-04-01
    ${gig_id}=    Set Variable    ${create.json()}[id]
    ${original_wage}=    Set Variable    ${create.json()}[wage]
    ${body}=    Create Dictionary    title=New Title
    ${response}=    PUT On Session    ${SESSION}    /gigs/${gig_id}    json=${body}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[title]    New Title
    Should Be Equal As Numbers    ${response.json()}[wage]    ${original_wage}

Update Gig Not Found
    [Documentation]    PUT on non-existent gig should return 404.
    ${body}=    Create Dictionary    title=Ghost Gig
    ${response}=    PUT On Session    ${SESSION}    /gigs/99999    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    404