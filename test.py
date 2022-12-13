import pytest
from menu_delivery import delivery
from PyInquirer import Validator, ValidationError


class document:
    """Sample class for temporary document object"""

    def __init__(self, text):
        """creates a text element

        Args:
            text (string): test string for any document object
        """
        self.text = text


def test_ip_standard():
    """Tests standard ip addresses"""
    IPValidator = delivery.IPValidator()
    test_ip_list = [
        document("127.0.0.1"),
        document("192.168.0.1"),
        document("172.168.1.4"),
        document("10.0.0.1"),
    ]
    for test_ip in test_ip_list:
        try:
            IPValidator.validate(test_ip)
        except Exception as exc:
            assert False


def test_ip_string():
    """Tests string in IP"""
    IPValidator = delivery.IPValidator()
    with pytest.raises(ValidationError):
        IPValidator.validate(document("asgsadfg"))


def test_ip_two_dots():
    """Tests incomplete IP"""
    IPValidator = delivery.IPValidator()
    with pytest.raises(ValidationError):
        IPValidator.validate(document("127.0.0"))


def test_ip_one_dot():
    """Tests incomplete IP"""
    IPValidator = delivery.IPValidator()
    with pytest.raises(ValidationError):
        IPValidator.validate(document("127.0"))


def test_ip_whole_number():
    """Tests incomplete IP"""
    IPValidator = delivery.IPValidator()
    with pytest.raises(ValidationError):
        IPValidator.validate(document("127"))


def test_ip_special_character():
    """Tests special characters in ip"""
    IPValidator = delivery.IPValidator()
    with pytest.raises(ValidationError):
        IPValidator.validate(document("##.##.##.##"))


def test_port_standard():
    """Tests standard port addresses"""
    PortValidator = delivery.PortValidator()
    test_port = document("10002")
    try:
        PortValidator.validate(test_port)
    except Exception as exc:
        assert False


def test_port_string():
    """Tests string in IP"""
    PortValidator = delivery.PortValidator()
    with pytest.raises(ValueError):
        PortValidator.validate(document("wefew"))


def test_port_bigger_than():
    """Tests bigger than 25565 port"""
    PortValidator = delivery.PortValidator()
    with pytest.raises(ValidationError):
        PortValidator.validate(document("25566"))


def test_port_smaller_than():
    """Tests smaller than 1 ports"""
    PortValidator = delivery.PortValidator()
    with pytest.raises(ValidationError):
        PortValidator.validate(document("0"))


def test_add_choices():
    """Tests the function add_choices"""
    questions = [
        {
            "type": "checkbox",
            "message": "Select toppings",
            "name": "toppings",
            "choices": [],
            "validate": lambda answer: "You must choose at least one topping."
            if len(answer) == 0
            else True,
        }
    ]
    category = "noodles"
    menu = {"noodles": [{"name": "Shin"}, {"name": "Jin"}, {"name": "Noguri"}]}
    delivery.CLI.menu = menu

    # get values from menu
    menu_items = []
    for item in menu[category]:
        menu_items.append(item["name"])

    # get values from add_choices
    add_choice_items = []
    for item in delivery.CLI.add_choices(delivery.CLI, questions, category)[0][
        "choices"
    ][1:]:
        add_choice_items.append(item["name"])

    assert add_choice_items == menu_items
