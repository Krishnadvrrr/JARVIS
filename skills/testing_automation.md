# Skill: Automated Testing & Verification
keywords: [testing, tests, unittest, pytest, verification, tdd, assertions, coverage]

## 1. Unit Test Structure
- Use Python's standard `unittest` library for zero external dependency testing.
- Name test files with `test_*.py` and test classes extending `unittest.TestCase`.
- Individual test methods must start with `test_*`.

## 2. Test Coverage & Edge Cases
- Test the "Happy Path": Valid inputs produce expected outputs.
- Test "Error Paths": Invalid inputs, missing arguments, or malformed data raise expected exceptions.
- Test "Boundary Conditions": Empty strings, zero, negative numbers, extreme inputs, null states.

## 3. Test Isolation & Cleanliness
- Tests must be deterministic: never depend on network calls or external shared state.
- Use `setUp()` and `tearDown()` to initialize and clean up test fixtures, in-memory databases, and temp files.
- Each test must run independently and assert clear outcomes.
