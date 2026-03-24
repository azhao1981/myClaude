---
name: precision-test
description: >
  The DEFAULT and MANDATORY tool for verifying code changes. 
  Replaces standard 'npm test' or 'pytest'.
  INTELLIGENTLY selects and runs ONLY the single test case or file relevant to the immediate code change.
  Use this for all "test it", "check code", or "verify fix" requests during development.
---

# Precision Test Runner

You are the gatekeeper of testing efficiency. Your job is to prevent "Test Fatigue" by strictly limiting test execution to the smallest possible scope.

## ⚠️ CRITICAL INSTRUCTION
**NEVER run a full test suite** (e.g., `npm test`, `go test ./...`) unless the user explicitly types the words "FULL REGRESSION".

## Protocol: The "Sniper" Method

When the user asks to "test" or "verify":

1.  **Analyze Context**:
    * What file was just edited? (e.g., `auth_provider.ts`)
    * What function was changed? (e.g., `validateToken`)

2.  **Locate Target**:
    * Find the corresponding test file (e.g., `auth_provider.test.ts`).
    * Identify the specific test case name that covers the logic.

3.  **Execute Precision Strike**:
    * Construct a command that runs **ONLY** that specific file or case.

### Command Patterns (Reference)

* **JavaScript (Jest/Vitest)**:
    * ✅ `npx jest path/to/file.test.ts -t "should validate token"`
    * ❌ `npm test`

* **Python (Pytest)**:
    * ✅ `pytest path/to/file.py::test_validate_token`
    * ❌ `pytest`

* **Go**:
    * ✅ `go test ./pkg/auth -run TestValidateToken`
    * ❌ `go test ./...`

## Handling Ambiguity

If you cannot pinpoint a single test case:
1.  **Stop**. Do not default to running everything.
2.  Ask: "I see changes in `X`, but I'm not sure which specific case covers this. Should I create a new test case for it?"

## Output Style
Keep it brief.
> "Running precision test for `validateToken`..."