# Common Root Cause Patterns in Software

Frequently encountered root causes when applying 5-Whys to software problems.

---

## Pattern 1: Missing Error Handling

### Typical Chain
```
Problem: Service returns 500 error intermittently
Why 1: Unhandled exception in payment processing
Why 2: External API returned unexpected format
Why 3: API version changed without notice
Why 4: No schema validation on API response
Why 5: Error handling assumes happy path only
```

### Root Cause Type
**Design Gap** - Defensive programming not applied

### Countermeasures
| Type | Action |
|------|--------|
| Immediate | Add try-catch, return graceful error |
| Preventive | Schema validation on all external inputs |
| Detection | Alert on unexpected response formats |

---

## Pattern 2: Resource Leaks

### Typical Chain
```
Problem: Application memory grows until OOM
Why 1: Heap usage increases over time
Why 2: Objects not garbage collected
Why 3: References held in static cache
Why 4: Cache has no eviction policy
Why 5: Cache designed for small dataset, now large
```

### Root Cause Type
**Scaling Assumption** - Design didn't account for growth

### Countermeasures
| Type | Action |
|------|--------|
| Immediate | Restart service, add memory |
| Preventive | LRU cache with size limits |
| Detection | Memory usage alerts at 80% |

---

## Pattern 3: Race Conditions

### Typical Chain
```
Problem: Duplicate orders created occasionally
Why 1: Same order inserted twice
Why 2: Two requests processed simultaneously
Why 3: No idempotency key check
Why 4: Assumed single request per order
Why 5: No distributed system thinking in design
```

### Root Cause Type
**Concurrency Gap** - Single-threaded assumptions in distributed system

### Countermeasures
| Type | Action |
|------|--------|
| Immediate | Database unique constraint |
| Preventive | Idempotency keys required |
| Detection | Duplicate detection in monitoring |

---

## Pattern 4: Configuration Drift

### Typical Chain
```
Problem: Feature works in staging, fails in prod
Why 1: Environment variable missing in prod
Why 2: Manual deployment missed the variable
Why 3: No config validation at startup
Why 4: No infrastructure-as-code for env vars
Why 5: Config management treated as afterthought
```

### Root Cause Type
**Process Gap** - Manual process where automation needed

### Countermeasures
| Type | Action |
|------|--------|
| Immediate | Add missing config |
| Preventive | IaC for all configuration |
| Detection | Config diff check in CI/CD |

---

## Pattern 5: Cascade Failures

### Typical Chain
```
Problem: All services down during traffic spik

