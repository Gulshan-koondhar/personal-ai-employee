---
type: social_media_approval_dashboard
generated: 2026-02-26T12:07:29.289075
---

# Social Media Approval Dashboard

## Status Overview

| Status | Count |
|--------|-------|
| 🔴 Pending Approval | 0 |
| 🟢 Approved | 1 |
| ❌ Rejected | 0 |
| ✅ Published | 1 |

## API Configuration

| Platform | Status |
|----------|--------|
| Twitter | ✅ Configured |
| LinkedIn | ✅ Configured |
| Facebook | ⚠️ Simulated (Manual) |
| Instagram | ⚠️ Simulated (Manual) |

## Workflow

1. **AI creates draft** → Social_Posts/
2. **Submit for approval** → Plans/Pending_Approval/Social_Media/
3. **Human reviews** → Move to Approved or Rejected
4. **Auto-publish** → If approved and API configured
5. **Archive** → Social_Posts/Published/

## Pending Approvals

*No pending approvals*

---
*Generated: 2026-02-26 12:07:29*
