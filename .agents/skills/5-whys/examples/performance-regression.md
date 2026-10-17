# Example: Performance Regression - API Latency Increase

A 5-Whys analysis tracing a performance degradation to its root cause.

---

## 5-Whys Analysis: Search API Latency Regression

### Problem Statement

| Field | Details |
|-------|---------|
| **What** | Search API p99 latency increased from 200ms to 800ms |
| **When** | First observed 2024-02-01, after v2.3.0 deployment |
| **Where** | search-service, all regions |
| **Duration** | Ongoing until fix deployed |
| **Impact** | User complaints, 15% drop in search usage |

### Detection Timeline

```
Feb 1, 10:00 - v2.3.0 deployed to production
Feb 1, 14:00 - Latency alert fires (p99 > 500ms)
Feb 1, 14:30 - Investigation begins
Feb 2, 09:00 - Root cause identified
Feb 2, 15:00 - Fix deployed, latency returns to normal
```

---

### Why Chain

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| **Why 1** | Why did search API latency increase 4x? | Database queries taking longer | Query timing metrics showed DB time 600ms vs 100ms before |
| **Why 2** | Why are database queries slower? | Full table scan on products table | EXPLAIN ANALYZE showed Seq Scan instead of Index Scan |
| **Why 3** | Why is a full table scan happening? | Query predicate changed, doesn't use index | Query plan shows index on `category_id` not being used |
| **Why 4** | Why doesn't the new query use the index? | New filter uses `LOWER(category_name)` instead of `category_id` | Code diff in v2.3.0 shows the change |
| **Why 5** | Why was this change made without index? | Developer assumed existing index covered it; no query review | PR #1847 shows no query plan check |

---

### Deeper Investigation

**Why was there no query review in PR #1847?**

| Level | Question | Answer |
|-------|----------|--------|
| Why 5a | Why no query review? | Team doesn't have query review checklist |
| Why 5b | Why no checklist? | Performance wasn't seen as critical for search |
| Why 5c | Why wasn't it seen as critical? | No SLO defined for search latency |

**Second Root Cause:** No performance SLO → No review process → Regression shipped

---

### Root Causes

**Primary Root Cause:**
Query changed to use `LOWER(category_name)` for case-insensitive search, but no functional index exists for that expression.

**Category:** Design Gap + Process Gap

**Seco

