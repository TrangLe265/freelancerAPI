*** Settings ***
Library    RequestsLibrary
Library    Collections

*** Variables ***
${BASE_URL}       http://127.0.0.1:8000
${SESSION}        api

*** Keywords ***
Create API Session
    Create Session    ${SESSION}    ${BASE_URL}

### --- CLIENT KEYWORDS ---

Create Client
    [Arguments]    ${name}    ${email}    ${phone}=${None}    ${business_id}=${None}    ${note}=${None}
    ${body}=    Create Dictionary    name=${name}    email=${email}
    IF    $phone is not None
        Set To Dictionary    ${body}    phone=${phone}
    END
    IF    $business_id is not None
        Set To Dictionary    ${body}    business_id=${business_id}
    END
    IF    $note is not None
        Set To Dictionary    ${body}    note=${note}
    END
    ${response}=    POST On Session    ${SESSION}    /clients/    json=${body}    expected_status=any
    RETURN    ${response}

Get All Clients
    ${response}=    GET On Session    ${SESSION}    /clients/
    RETURN    ${response}

Get Client By ID
    [Arguments]    ${client_id}
    ${response}=    GET On Session    ${SESSION}    /clients/${client_id}    expected_status=any
    RETURN    ${response}

### --- GIG KEYWORDS ---

Create Gig
    [Arguments]    ${client_id}    ${title}    ${wage}    ${date}    ${location}=${None}    ${description}=${None}
    ${body}=    Create Dictionary    client_id=${client_id}    title=${title}    wage=${wage}    date=${date}
    IF    $location is not None
        Set To Dictionary    ${body}    location=${location}
    END
    IF    $description is not None
        Set To Dictionary    ${body}    description=${description}
    END
    ${response}=    POST On Session    ${SESSION}    /gigs/    json=${body}    expected_status=any
    RETURN    ${response}

Get Gig By ID
    [Arguments]    ${gig_id}
    ${response}=    GET On Session    ${SESSION}    /gigs/${gig_id}    expected_status=any
    RETURN    ${response}

### --- INVOICE KEYWORDS ---

Create Invoice
    [Arguments]    ${client_id}    ${gig_id}    ${issue_date}    ${due_date}    ${status}=draft
    ${body}=    Create Dictionary
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=${issue_date}
    ...    due_date=${due_date}
    ...    status=${status}
    ${response}=    POST On Session    ${SESSION}    /invoices/    json=${body}    expected_status=any
    RETURN    ${response}

Get Invoice By ID
    [Arguments]    ${invoice_id}
    ${response}=    GET On Session    ${SESSION}    /invoices/${invoice_id}    expected_status=any
    RETURN    ${response}