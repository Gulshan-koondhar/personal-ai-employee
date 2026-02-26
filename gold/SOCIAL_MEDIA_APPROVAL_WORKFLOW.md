# Social Media Approval Workflow

## Overview

The Personal AI Employee now includes a **Human-in-the-Loop (HITL) approval workflow** for social media posting. This ensures that all posts are reviewed by a human before being published, preventing accidental or inappropriate posts.

---

## 🔄 Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Social Media Posting Workflow                │
└─────────────────────────────────────────────────────────────────┘

1. AI creates draft post
   └─→ Social_Posts/FB_POST_*.md (or IG_POST_, TWITTER_POST_)

2. AI submits for approval
   └─→ Plans/Pending_Approval/Social_Media/SOCIAL_APPROVAL_*.md

3. Human reviews the approval request
   └─→ Reads post content and business reason

4. Human makes decision:
   
   ✅ APPROVE:
   └─→ Move file to Plans/Approved/Social_Media/
       └─→ Auto-publishes (if API configured)
           └─→ Moves to Social_Posts/Published/
   
   ❌ REJECT:
   └─→ Move file to Plans/Rejected/Social_Media/
       └─→ Post is not published
   
   ✏️ MODIFY:
   └─→ Edit source post file
       └─→ Delete approval request
           └─→ Re-submit for approval
```

---

## 📁 Directory Structure

```
AI_Employee_Vault/
├── Social_Posts/
│   ├── FB_POST_*.md              # Facebook drafts
│   ├── IG_POST_*.md              # Instagram drafts
│   ├── TWITTER_POST_*.md         # Twitter drafts
│   ├── LINKEDIN_POST_*.md        # LinkedIn drafts
│   ├── Published/                # Successfully published posts
│   └── APPROVAL_DASHBOARD.md     # Current approval status
│
└── Plans/
    ├── Pending_Approval/
    │   └── Social_Media/         # Awaiting human review
    ├── Approved/
    │   └── Social_Media/         # Approved, ready to publish
    └── Rejected/
        └── Social_Media/         # Rejected posts
```

---

## 🚀 Usage

### For Users (Approvers)

1. **Check for pending approvals:**
   - Open `AI_Employee_Vault/Plans/Pending_Approval/Social_Media/`
   - Review any `SOCIAL_APPROVAL_*.md` files

2. **Review the post:**
   - Open the approval request file
   - Read the post content and business reason

3. **Make a decision:**
   - **Approve:** Move file to `Plans/Approved/Social_Media/`
   - **Reject:** Move file to `Plans/Rejected/Social_Media/`
   - **Modify:** Edit source file, delete approval, re-submit

4. **Auto-publish happens automatically:**
   - Run: `python gold/social_media_approval.py`
   - Or wait for scheduled orchestrator run

---

### For Developers

#### Submit a Post for Approval

```python
from pathlib import Path
from social_integration import SocialMediaIntegrator

vault_path = Path("../AI_Employee_Vault")
integrator = SocialMediaIntegrator(str(vault_path))

# Create a draft post
fb_post = integrator.create_facebook_post(
    "Exciting business update! #Innovation",
    "images/milestone.jpg"
)

# Submit for approval
post_file = vault_path / "Social_Posts" / fb_post['post_id']
approval = integrator.submit_post_for_approval(
    post_file,
    reason="Business update to generate client interest"
)
```

#### Process Approved Posts

```python
from social_media_approval import SocialMediaApprovalWorkflow

workflow = SocialMediaApprovalWorkflow(str(vault_path))

# Process all approved posts
results = workflow.process_approved_posts()
print(f"Published: {results['published']}")
print(f"Failed: {results['failed']}")
```

#### Check Approval Status

```python
status = workflow.get_approval_status()
print(f"Pending: {status['pending']}")
print(f"Approved: {status['approved']}")
print(f"Rejected: {status['rejected']}")
print(f"Published: {status['published']}")
```

---

## 🔧 API Configuration

For **auto-publishing** to work, configure API credentials in `gold/.env`:

### Twitter (X)
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### LinkedIn
```env
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_PERSON_URN=urn:li:person:YOUR_ID
```

### Facebook & Instagram
Currently **simulated** (manual posting required). Meta Graph API integration can be added.

---

## 📊 Approval Dashboard

The system automatically generates an approval dashboard at:
`AI_Employee_Vault/Social_Posts/APPROVAL_DASHBOARD.md`

This shows:
- Pending approvals count
- Approved count
- Rejected count
- Published count
- API configuration status
- List of pending approvals

---

## ✅ Hackathon Compliance

This approval workflow satisfies the hackathon requirements:

| Tier | Requirement | Implementation |
|------|-------------|----------------|
| **Silver** | Automatically Post on LinkedIn | ✅ Creates drafts + approval workflow |
| **Gold** | Facebook & Instagram post | ✅ Creates drafts + approval workflow |
| **Gold** | Twitter (X) post | ✅ Creates drafts + approval workflow |
| **Platinum** | Draft-only, Local approval | ✅ **Fully compliant** |

**Note:** The Platinum tier explicitly states:
> "Cloud owns: social post drafts/scheduling (**draft-only; requires Local approval before send/post**)"

Our implementation follows this architecture exactly.

---

## 🔒 Safety Features

1. **No accidental posts:** All posts require human approval
2. **Audit trail:** All approvals/rejections are logged
3. **Business justification:** Each post includes a reason
4. **Easy modification:** Can edit and re-submit if changes needed
5. **Platform separation:** Each platform handled independently

---

## 📝 Example Approval Request

```markdown
---
type: social_media_approval
platform: facebook
status: pending
created: 2026-02-26T11:32:52
source_file: Social_Posts/FB_POST_20260226_113252.md
reason: Business update to generate client interest and sales
---

# Social Media Approval Request

## Platform
**FACEBOOK**

## Post Content
```
🚀 Excited to announce our latest project milestone! 
Our team has been working hard to deliver exceptional results. 
#Innovation #Business
```

## Instructions
- **To Approve:** Move to `Plans/Approved/Social_Media/`
- **To Reject:** Move to `Plans/Rejected/Social_Media/`
- **To Modify:** Edit source file and re-submit
```

---

## 🎯 Best Practices

1. **Review before approving:** Always read the full post content
2. **Check timing:** Consider if now is the right time to post
3. **Verify hashtags:** Ensure they're appropriate for your brand
4. **Monitor engagement:** Check published posts for responses
5. **Keep audit trail:** Don't delete approval files after processing

---

*Generated: February 26, 2026*  
*Personal AI Employee - Human-in-the-Loop Social Media Posting*
