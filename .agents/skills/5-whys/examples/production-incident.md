# Example: Production Incident - Payment Service Outage

A complete 5-Whys analysis of a production payment service failure.

---

## 5-Whys Analysis: Payment Service Outage (2024-01-15)

### Problem Statement

| Field | Details |
|-------|---------|
| **What** | Payment API returning 503 errors, all transactions failing |
| **When** | 2024-01-15, 14:23 UTC, during peak traffic |
| **Where** | payment-service in production (us-east-1) |
| **Duration** | 47 minutes |
| **Impact** | ~$150,000 in failed transactions, 12,000 affected users |

### Timeline

```
14:23 - First 503 errors appear in monitoring
14:25 - Alert fires: payment-service error rate > 5%
14:28 - On-call engineer begins investigation
14:35 - Identified: all DB connections exhausted
14:42 - Attempted restart, problem persists
14:55 - Root cause identified: connection leak
15:02 - Hotfix deployed
15:10 - Service fully recovered
```

---

### Why Chain

| Level | Question | Answer | Evidence |
|-------|----------|--------|----------|
| **Why 1** | Why did the payment API return 503 errors? | Database connection pool was exhausted (0/100 available) | Connection pool metrics showed 100/100 in use |
| **Why 2** | Why was the connection pool exhausted? | Connections were being acquired but not released | Connection age histogram showed connections held for hours |
| **Why 3** | Why were connections not being released? | Exception thrown before connection.close() in refund handler | Stack trace in logs showed exception at line 142 |
| **Why 4** | Why did the exception prevent connection close? | No try-finally block; close() only in happy path | Code inspection of RefundHandler.java |
| **Why 5** | Why was there no try-finally block? | Code copied from old service that used auto-commit (no explicit close needed) | Git blame showed copy-paste from legacy service |

---

### Root Cause

**Identified Cause:** Connection handling code was copied from a legacy service that used auto-commit mode (where connections auto-close). The new service uses manual transactions, requiring explicit close(), but the code pattern wasn't updated.

**Category:** Design Gap (incorrect pattern a

