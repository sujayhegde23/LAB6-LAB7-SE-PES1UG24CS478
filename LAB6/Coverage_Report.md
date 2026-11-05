# Lab 6: Code and Branch Coverage Analysis Report

## Student Details
- **Repository**: [LAB6-LAB7-SE-PES1UG24CS478](https://github.com/sujayhegde23/LAB6-LAB7-SE-PES1UG24CS478.git)
- **Application Under Test**: `LAB6/museum_admission.py`

---

## 1. Objectives & Concepts

- **Line Coverage (Statement Coverage)**: Measures whether each executable line of source code was executed at least once during test execution. While it ensures that no lines are dead code, it does not guarantee that every decision or alternate logic branch is verified.
- **Branch Coverage**: Measures whether every decision point / control structure (e.g. `if`, `elif`, `else`, boolean conditions) evaluated to both `True` and `False`. This ensures that all logical branches and edge case pathways are thoroughly tested.

---

## 2. Initial Test Case Coverage (Baseline)

### Initial Run:
- Initial test file: `test_museum_admission.py` (contained only 2 starter tests: `test_adult_weekday` and `test_small_group`).
- **Initial Line Coverage**: 47% (19 statements missed out of 36).
- **Initial Branch Coverage**: 42% (10 partial branches missed).

---

## 3. Code Coverage Analysis (>90% Achieved)

### Test Suite: `CodeCoverageTest_museum_admission.py`
Targeted test cases were added to ensure every statement and branch in `ticket_price()`, `group_discount()`, and `gallery_entry()` is executed:
- **`test_ticket_price_unknown_category`**: Tests invalid category exception (`ValueError`).
- **`test_ticket_price_negative_age`**: Tests negative age validation (`ValueError`).
- **`test_ticket_price_child_under_5`**: Tests free entry for children under 5.
- **`test_ticket_price_monday_student_guided_tour`**: Tests Monday 50% discount and student guided tour surcharge.
- **`test_ticket_price_saturday_adult_guided_tour`**: Tests weekend surcharge and adult guided tour fee.
- **`test_group_discount_invalid_size`**: Tests invalid group size `< 1` (`ValueError`).
- **`test_group_discount_school_large`**: Tests school group `>= 20` (40% discount).
- **`test_group_discount_school_small`**: Tests school group `< 20` (25% discount).
- **`test_group_discount_regular_large`**: Tests regular group `>= 15` (20% discount).
- **`test_group_discount_regular_medium`**: Tests regular group `>= 8` (10% discount).
- **`test_group_discount_regular_small`**: Tests regular group `< 8` (0% discount).
- **`test_gallery_entry_wait`**: Tests entry when gallery is at capacity.
- **`test_gallery_entry_queue`**: Tests entry when gallery is near capacity (>= 90%) without a timed slot.
- **`test_gallery_entry_enter`**: Tests regular entry when below capacity threshold.

### Coverage Result:
```
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
CodeCoverageTest_museum_admission.py      37      0   100%
museum_admission.py                       36      0   100%
--------------------------------------------------------------------
TOTAL                                     73      0   100%
```
- **Line Coverage Achieved**: **100%** (Well above the required 90%).

### Terminal Output Screenshot:
![Code Coverage Report](code_coverage_analysis.png)
