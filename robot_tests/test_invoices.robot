*** Settings ***
Resource          resources/common.resource
Suite Setup       Create API Session

*** Keywords ***
Create Test Client And Gig
    [Documentation]    Helper to create a client and gig, returns both IDs as a list.
    ${client_response}=    Create Client    name=Invoice Test Client    email=invoicetest_robot@example.com
    ${client_id}=    Set Variable    ${client_response.json()}[id]
    ${gig_response}=    Create Gig
    ...    client_id=${client_id}
    ...    title=Invoice Test Gig
    ...    wage=${1500}
    ...    date=2026-03-01
    ${gig_id}=    Set Variable    ${gig_response.json()}[id]
    RETURN    ${client_id}    ${gig_id}

*** Test Cases ***

# -------------------------------------------------------
# CREATE INVOICE
# -------------------------------------------------------

Create Invoice Successfully
    [Documentation]    Happy path: valid invoice linked to existing client and gig.
    ${client_id}    ${gig_id}=    Create Test Client And Gig
    ${response}=    Create Invoice
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    Should Be Equal As Integers    ${response.status_code}    200
    ${data}=    Set Variable    ${response.json()}
    Should Be Equal    ${data}[status]    draft
    Should Be Equal As Integers    ${data}[client_id]    ${client_id}
    Should Be Equal As Integers    ${data}[gig_id]    ${gig_id}
    Dictionary Should Contain Key    ${data}    id

Invoice Total Amount Matches Gig Wage
    [Documentation]    total_amount in invoice response should equal the linked gig wage.
    ${client_id}    ${gig_id}=    Create Test Client And Gig
    ${response}=    Create Invoice
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    Should Be Equal As Numbers    ${response.json()}[total_amount]    1500

Create Invoice With Invalid Status
    [Documentation]    Invalid status value should return 422.
    ${client_id}    ${gig_id}=    Create Test Client And Gig
    ${body}=    Create Dictionary
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    ...    status=nonexistent_status
    ${response}=    POST On Session    ${SESSION}    /invoices/    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    422

Create Invoice Missing Client ID
    [Documentation]    Missing client_id should return 422.
    ${body}=    Create Dictionary
    ...    gig_id=${1}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    ...    status=draft
    ${response}=    POST On Session    ${SESSION}    /invoices/    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    422

# -------------------------------------------------------
# GET INVOICE
# -------------------------------------------------------

Get Invoice By Valid ID
    [Documentation]    Should return the correct invoice when given a valid ID.
    ${client_id}    ${gig_id}=    Create Test Client And Gig
    ${create}=    Create Invoice
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    ${invoice_id}=    Set Variable    ${create.json()}[id]
    ${response}=    Get Invoice By ID    ${invoice_id}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal As Integers    ${response.json()}[id]    ${invoice_id}

Get Invoice By Invalid ID
    [Documentation]    Non-existent invoice ID should return 404.
    ${response}=    Get Invoice By ID    99999
    Should Be Equal As Integers    ${response.status_code}    404

# -------------------------------------------------------
# UPDATE INVOICE STATUS
# -------------------------------------------------------

Update Invoice Status To Sent
    [Documentation]    Should progress invoice status from draft to sent.
    ${client_id}    ${gig_id}=    Create Test Client And Gig
    ${create}=    Create Invoice
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    ${invoice_id}=    Set Variable    ${create.json()}[id]
    ${body}=    Create Dictionary    status=sent
    ${response}=    PUT On Session    ${SESSION}    /invoices/${invoice_id}    json=${body}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[status]    sent

Update Invoice Status To Paid
    [Documentation]    Should mark invoice as paid.
    ${client_id}    ${gig_id}=    Create Test Client And Gig
    ${create}=    Create Invoice
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    ${invoice_id}=    Set Variable    ${create.json()}[id]
    ${body}=    Create Dictionary    status=paid
    ${response}=    PUT On Session    ${SESSION}    /invoices/${invoice_id}    json=${body}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[status]    paid

Update Invoice Status To Void
    [Documentation]    Should allow voiding an invoice.
    ${client_id}    ${gig_id}=    Create Test Client And Gig
    ${create}=    Create Invoice
    ...    client_id=${client_id}
    ...    gig_id=${gig_id}
    ...    issue_date=2026-03-01
    ...    due_date=2026-03-16
    ${invoice_id}=    Set Variable    ${create.json()}[id]
    ${body}=    Create Dictionary    status=void
    ${response}=    PUT On Session    ${SESSION}    /invoices/${invoice_id}    json=${body}
    Should Be Equal As Integers    ${response.status_code}    200
    Should Be Equal    ${response.json()}[status]    void

Update Invoice Not Found
    [Documentation]    PUT on non-existent invoice should return 404.
    ${body}=    Create Dictionary    status=paid
    ${response}=    PUT On Session    ${SESSION}    /invoices/99999    json=${body}    expected_status=any
    Should Be Equal As Integers    ${response.status_code}    404