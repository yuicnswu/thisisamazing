---
name: 5-whys
description: This skill should be used when the user asks to "find the root cause", "找根因", "为什么会出现这个问题", "why did this happen", "debug this issue", "排查问题", "analyze this bug", "分析这个bug", "what's causing this", "问题出在哪", "dig deeper", "深挖原因", or needs to systematically trace a problem back to its fundamental cause rather than just addressing symptoms.
version: 0.1.0
---

# 5-Whys Root Cause Analysis

A systematic technique for drilling down through symptoms to uncover the true root cause of a problem by repeatedly asking "Why?" until the fundamental issue is revealed.

## When to Use This Skill

- Bug investigation where the obvious fix didn't work
- Production incidents requiring post-mortem analysis
- Performance problems with unclear origins
- Recurring issues that keep coming back after "fixes"
- System failures requiring prevention, not just recovery
- Any situation where treating symptoms isn't enough

## Core Process

### Phase 1: Define the Problem Clearly

State the problem as a specific, observable fact:

**Good problem statements:**
- "The API response time increased from 50ms to 500ms"
- "Users are seeing 500 errors on the checkout page"
- "The nightly job failed at 3:00 AM"

**Poor problem statements:**
- "The system is slow" (too vague)
- "Something is broken" (not specific)
- "Users are unhappy" (symptom, not problem)

**Problem Statement Template:**
```
What: [Specific observable behavior]
When: [Time/conditions when it occurs]
Where: [Component/system affected]
Impact: [Measurable consequence]
```

### Phase 2: Ask "Why?" Iteratively

For each answer, ask "Why does that happen?" until reaching an actionable root cause:

**The 5-Whys Chain:**
```
Problem: [Statement]
    ↓
Why 1: [First-level cause]
    ↓
Why 2: [Deeper cause]
    ↓
Why 3: [Even deeper]
    ↓
Why 4: [Approaching root]
    ↓
Why 5: [Root cause - actionable]
```

**Quality Checks for Each "Why":**
- Is this answer factual and verifiable?
- Does this explain the previous level?
- Is there evidence supporting this?
- Could there be multiple causes at this level?

### Phase 3: Identify the Root Cause

A true root cause has these characteristics:

| Characteristic | Test |
|----------------|------|
| **Actionable** | Can we do something about it? |
| **Preventable** | Would fixing this prevent recurrence? |
| **Fundamental** | Asking "why" again yields nothing actionable |
| **Verifiable** | Can we prove this is the cause? |

**Stop Conditions:**
- Reached a process/policy that can be changed
- Found a missing control or check
- Identified a knowledge/training gap
- Discovered a design flaw
- Hit a resource constraint decision

### Phase 4: Validate the Chain

Work backwards through the chain:

```
If [Root Cause] is fixed
→ Then [Why 4] wouldn't happen
→ Then [Why 3] wouldn't happen
→ Then [Why 2] wouldn't happen
→ Then [Why 1] wouldn't happen
→ Then [Problem] wouldn't occur
```

If the chain breaks at any point, revisit that level.

### Phase 5: Define Countermeasures

For the root cause, define:

1. **Immediate fix** - Stop the bleeding
2. **Preventive measure** - Ensure it never happens again
3. **Detection mechanism** - Catch it early if prevention 

