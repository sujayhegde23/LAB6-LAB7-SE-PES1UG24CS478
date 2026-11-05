import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ============================================================================
# 1. INITIAL EXAMPLE TEST CASES
# ============================================================================

def test_adult_weekday():
    """Initial test: adult ticket on a weekday without guided tour."""
    assert ticket_price("adult", 30, "tuesday", False) == 300


def test_small_group():
    """Initial test: small non-school group (< 8) receiving 0 discount."""
    assert group_discount(4, False) == 0


# ============================================================================
# 2. BRANCH COVERAGE TEST CASES: ticket_price
# ============================================================================

def test_ticket_price_unknown_category_branch():
    """Branch: category not in BASE_PRICE -> ValueError."""
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 25, "monday", False)


def test_ticket_price_negative_age_branch():
    """Branch: age < 0 -> ValueError."""
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "monday", False)


def test_ticket_price_child_under_5_boundaries():
    """Branch: age < 5 -> returns 0 (tested at age 0 and age 4)."""
    assert ticket_price("child", 0, "wednesday", False) == 0
    assert ticket_price("child", 4, "sunday", True) == 0


def test_ticket_price_age_5_boundary_not_free():
    """Branch: age < 5 is False (boundary at age 5, regular child ticket)."""
    # Child base price: 100, weekday, no tour
    assert ticket_price("child", 5, "wednesday", False) == 100


def test_ticket_price_all_categories_pricing():
    """Verify base prices for all supported categories."""
    assert ticket_price("adult", 25, "wednesday", False) == 300
    assert ticket_price("student", 20, "thursday", False) == 150
    assert ticket_price("child", 10, "friday", False) == 100
    assert ticket_price("senior", 65, "tuesday", False) == 200


def test_ticket_price_monday_discount_branch():
    """Branch: day == 'monday' -> price // 2."""
    # Adult: 300 // 2 = 150
    assert ticket_price("adult", 30, "monday", False) == 150
    # Student: 150 // 2 = 75
    assert ticket_price("student", 20, "monday", False) == 75


def test_ticket_price_saturday_surcharge_branch():
    """Branch: day in ('saturday', 'sunday') -> True for 'saturday' (+50)."""
    # Adult base 300 + 50 = 350
    assert ticket_price("adult", 30, "saturday", False) == 350


def test_ticket_price_sunday_surcharge_branch():
    """Branch: day in ('saturday', 'sunday') -> True for 'sunday' (+50)."""
    # Senior base 200 + 50 = 250
    assert ticket_price("senior", 68, "sunday", False) == 250


def test_ticket_price_student_guided_tour_branch():
    """Branch: with_guided_tour is True AND category == 'student' (+50)."""
    # Student base 150 + 50 tour = 200
    assert ticket_price("student", 22, "tuesday", True) == 200
    # Student on Monday: 150 // 2 = 75 + 50 tour = 125
    assert ticket_price("student", 22, "monday", True) == 125


def test_ticket_price_non_student_guided_tour_branch():
    """Branch: with_guided_tour is True AND category != 'student' (+100)."""
    # Adult weekday with tour: 300 + 100 = 400
    assert ticket_price("adult", 40, "thursday", True) == 400
    # Senior on Sunday with tour: 200 + 50 (weekend) + 100 (tour) = 350
    assert ticket_price("senior", 70, "sunday", True) == 350


# ============================================================================
# 3. BRANCH COVERAGE TEST CASES: group_discount
# ============================================================================

def test_group_discount_invalid_size_branches():
    """Branch: group_size < 1 -> ValueError (tested for 0 and negative)."""
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(-10, True)


def test_group_discount_school_large_branches():
    """Branch: is_school is True AND group_size >= 20 -> 40."""
    assert group_discount(20, True) == 40  # Boundary 20
    assert group_discount(30, True) == 40  # Above 20


def test_group_discount_school_small_branches():
    """Branch: is_school is True AND group_size < 20 -> 25."""
    assert group_discount(19, True) == 25  # Boundary 19
    assert group_discount(1, True) == 25   # Minimum valid group


def test_group_discount_regular_large_branches():
    """Branch: is_school is False AND group_size >= 15 -> 20."""
    assert group_discount(15, False) == 20  # Boundary 15
    assert group_discount(22, False) == 20  # Above 15


def test_group_discount_regular_medium_branches():
    """Branch: is_school is False AND 8 <= group_size < 15 -> 10."""
    assert group_discount(14, False) == 10  # Boundary 14
    assert group_discount(8, False) == 10   # Boundary 8


def test_group_discount_regular_small_branches():
    """Branch: is_school is False AND group_size < 8 -> 0."""
    assert group_discount(7, False) == 0  # Boundary 7
    assert group_discount(1, False) == 0  # Boundary 1


# ============================================================================
# 4. BRANCH COVERAGE TEST CASES: gallery_entry
# ============================================================================

def test_gallery_entry_at_capacity_branch():
    """Branch: visitors_inside >= capacity -> 'wait' (tested at equal & above)."""
    assert gallery_entry(100, 100, False) == "wait"
    assert gallery_entry(100, 100, True) == "wait"
    assert gallery_entry(105, 100, False) == "wait"


def test_gallery_entry_near_capacity_no_timed_slot_branch():
    """Branch: >= 90% capacity AND not has_timed_slot (both True) -> 'queue'."""
    assert gallery_entry(90, 100, False) == "queue"  # Boundary exactly 90%
    assert gallery_entry(95, 100, False) == "queue"  # 95%


def test_gallery_entry_near_capacity_with_timed_slot_branch():
    """Branch: >= 90% capacity BUT has_timed_slot is True -> 'enter' (skips queue)."""
    assert gallery_entry(90, 100, True) == "enter"  # Exactly 90% with timed slot
    assert gallery_entry(99, 100, True) == "enter"  # 99% with timed slot


def test_gallery_entry_below_capacity_branches():
    """Branch: < 90% capacity -> 'enter' regardless of timed slot."""
    assert gallery_entry(89, 100, False) == "enter"  # Boundary 89% without timed slot
    assert gallery_entry(89, 100, True) == "enter"   # Boundary 89% with timed slot
    assert gallery_entry(0, 100, False) == "enter"    # Empty gallery
