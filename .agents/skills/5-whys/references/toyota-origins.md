# 5-Whys: Toyota Origins and Principles

The history and core principles of 5-Whys from the Toyota Production System.

---

## Historical Background

### Origin
The 5-Whys technique was developed by **Sakichi Toyoda** (founder of Toyota Industries) and later refined by **Taiichi Ohno** as a critical component of the Toyota Production System (TPS) in the 1950s.

### The Famous Example

Taiichi Ohno's classic example from the factory floor:

```
Problem: The robot stopped working

Why 1: Why did the robot stop?
→ The circuit has overloaded, causing a fuse to blow.

Why 2: Why is the circuit overloaded?
→ There was insufficient lubrication on the bearings, so they locked up.

Why 3: Why was there insufficient lubrication?
→ The oil pump on the robot is not circulating sufficient oil.

Why 4: Why is the pump not circulating sufficient oil?
→ The pump intake is clogged with metal shavings.

Why 5: Why is the intake clogged with metal shavings?
→ There is no filter on the pump.

Root Cause: No filter on the oil pump intake
Solution: Install a filter on the oil pump
```

**Key Insight:** Without 5-Whys, the "fix" would have been replacing the fuse—and the robot would fail again.

---

## Core Principles from Toyota

### Principle 1: Go and See (Genchi Genbutsu)

**Definition:** Go to the actual place, see the actual situation, understand the actual facts.

**Application to 5-Whys:**
- Don't analyze from reports alone
- Verify each "why" with direct observation
- Evidence must be firsthand, not hearsay

**Software Equivalent:**
- Read the actual logs, not summaries
- Check the actual code, not just the description
- Verify in the actual environment where the problem occurred

### Principle 2: Respect for People

**Definition:** Problems are process problems, not people problems.

**Application to 5-Whys:**
- Never stop at "human error" as root cause
- Ask "why did the process allow this error?"
- Build systems that make errors impossible or obvious

**The Toyota Philosophy:**
> "Blame the process, not the person. Every defect is a gift—it reveals a weakness in our process that we can improve."

### Principle 3: Continuous Improvement (Kaizen)

**Definition:** Small, incremental improvements every day.

**Application to 5-Whys:**
- Each root cause found is an improvement opportunity
- Document learnings for future reference
- Share findings across teams

### Principle 4: Build Quality In (Jidoka)

**Definition:** Stop and fix problems when they occur, don't pass them on.

**Application to 5-Whys:**
- Address root causes immediately
- Prevention > detection > reaction
- Make problems visible

---

## The "5" in 5-Whys

### Why Specifically Five?

**Short Answer:** Five is a guideline, not a rule.

**Ohno's Observation:**
> "By asking 'why' five times, the nature of the problem as well as its solution becomes clear."

**The Reality:**
- Some problems need only 3 whys
- Some need 7 or more
- Stop when you reach an actionable root cause

### Signs You've Gone Deep Enough

| Signal | Example |
|--------|---------|
| Reached a process/policy | "No code review requirement" |
| Found a missing control | "No input validation" |
| Hit a design decision | "Chose eventual consistency" |
| Discovered a trade-

