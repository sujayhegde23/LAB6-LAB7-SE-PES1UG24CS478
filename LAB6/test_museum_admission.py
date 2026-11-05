import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ============================================================================
# Initial Example Test Cases
# ============================================================================

def test_adult_weekday():
    """Initial test: adult ticket on a weekday without guided tour."""
    assert ticket_price("adult", 30, "tuesday", False) == 300


def test_small_group():
    """Initial test: small non-school group (< 8) receiving 0 discount."""
    assert group_discount(4, False) == 0


# ============================================================================
# Additional Comprehensive Test Cases (100% Line & 100% Branch Coverage)
# ============================================================================

# --- ticket_price ---
def test_ticket_price_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 25, "monday", False)


def test_ticket_price_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "monday", False)


def test_ticket_price_child_under_5():
    assert ticket_price("child", 0, "wednesday", False) == 0
    assert ticket_price("child", 4, "sunday", True) == 0


def test_ticket_price_age_5_boundary():
    assert ticket_price("child", 5, "wednesday", False) == 100


def test_ticket_price_categories():
    assert ticket_price("adult", 25, "wednesday", False) == 300
    assert ticket_price("student", 20, "thursday", False) == 150
    assert ticket_price("child", 10, "friday", False) == 100
    assert ticket_price("senior", 65, "tuesday", False) == 200


def test_ticket_price_monday():
    assert ticket_price("adult", 30, "monday", False) == 150
    assert ticket_price("student", 20, "monday", False) == 75


def test_ticket_price_saturday():
    assert ticket_price("adult", 30, "saturday", False) == 350


def test_ticket_price_sunday():
    assert ticket_price("senior", 68, "sunday", False) == 250


def test_ticket_price_student_tour():
    assert ticket_price("student", 22, "tuesday", True) == 200
    assert ticket_price("student", 22, "monday", True) == 125


def test_ticket_price_non_student_tour():
    assert ticket_price("adult", 40, "thursday", True) == 400
    assert ticket_price("senior", 70, "sunday", True) == 350


# --- group_discount ---
def test_group_discount_invalid_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(-10, True)


def test_group_discount_school_large():
    assert group_discount(20, True) == 40
    assert group_discount(30, True) == 40


def test_group_discount_school_small():
    assert group_discount(19, True) == 25
    assert group_discount(1, True) == 25


def test_group_discount_regular_large():
    assert group_discount(15, False) == 20
    assert group_discount(22, False) == 20


def test_group_discount_regular_medium():
    assert group_discount(14, False) == 10
    assert group_discount(8, False) == 10


def test_group_discount_regular_small():
    assert group_discount(7, False) == 0
    assert group_discount(1, False) == 0


# --- gallery_entry ---
def test_gallery_entry_capacity():
    assert gallery_entry(100, 100, False) == "wait"
    assert gallery_entry(100, 100, True) == "wait"
    assert gallery_entry(105, 100, False) == "wait"


def test_gallery_entry_near_capacity_no_slot():
    assert gallery_entry(90, 100, False) == "queue"
    assert gallery_entry(95, 100, False) == "queue"


def test_gallery_entry_near_capacity_with_slot():
    assert gallery_entry(90, 100, True) == "enter"
    assert gallery_entry(99, 100, True) == "enter"


def test_gallery_entry_below_capacity():
    assert gallery_entry(89, 100, False) == "enter"
    assert gallery_entry(89, 100, True) == "enter"
    assert gallery_entry(0, 100, False) == "enter"
