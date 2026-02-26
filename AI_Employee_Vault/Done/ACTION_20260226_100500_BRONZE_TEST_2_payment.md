---
type: payment_request
amount: 250.00
recipient: Test Vendor
priority: high
status: pending
created: 2026-02-26T10:05:00
---

# Bronze Tier Test 2: Approval Workflow

## Payment Details
- **Amount:** $250.00
- **Recipient:** Test Vendor
- **Reason:** Software subscription payment
- **Invoice:** #TEST-001

## Approval Required
This payment requires human approval before processing.

## Test Steps
1. Orchestrator should detect payment keywords
2. Create approval request in Pending_Approval
3. Wait for human to move to Approved or Rejected
4. Process accordingly

## Expected Result
- Approval request file created in Plans/Pending_Approval
- File waits for human decision

## Test Status
- [ ] Payment file created in Needs_Action
- [ ] Approval request generated
- [ ] File in Pending_Approval folder
- [ ] Test PASSED


## Processing Log
- [x] Processed at 2026-02-26 11:03:45
- [x] Plan created and moved to Done folder