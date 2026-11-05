import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# --- Initial Example Test Cases ---
def test_adult_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300


def test_small_group():
    assert group_discount(4, False) == 0


# --- Code Coverage Test Cases for ticket_price ---
def test_ticket_price_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("foreigner", 25, "monday", False)


def test_ticket_price_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -5, "monday", False)


def test_ticket_price_child_under_5():
    assert ticket_price("child", 3, "monday", False) == 0


def test_ticket_price_monday_student_guided_tour():
    # Base: 150, Monday: 150 // 2 = 75, Student guided tour: +50 -> 125
    assert ticket_price("student", 20, "monday", True) == 125


def test_ticket_price_saturday_adult_guided_tour():
    # Base: 300, Saturday: +50, Adult guided tour: +100 -> 450
    assert ticket_price("adult", 35, "saturday", True) == 450


# --- Code Coverage Test Cases for group_discount ---
def test_group_discount_invalid_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


def test_group_discount_school_large():
    assert group_discount(20, True) == 40


def test_group_discount_school_small():
    assert group_discount(10, True) == 25


def test_group_discount_regular_large():
    assert group_discount(15, False) == 20


def test_group_discount_regular_medium():
    assert group_discount(8, False) == 10


def test_group_discount_regular_small():
    assert group_discount(5, False) == 0


# --- Code Coverage Test Cases for gallery_entry ---
def test_gallery_entry_wait():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_entry_queue():
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_entry_enter():
    assert gallery_entry(50, 100, False) == "enter"
