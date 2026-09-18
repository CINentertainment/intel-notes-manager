import unittest
from unittest.mock import patch

from validation import (
    credibility_description,
    get_classification,
    get_credibility,
    get_discipline,
    get_reliability,
    get_required_input,
    get_valid_date,
    reliability_description
)


class TestValidation(unittest.TestCase):

    def test_required_input_accepts_valid_text(self):
        with patch("builtins.input", return_value="Test Report"):
            result = get_required_input("Title: ")

        self.assertEqual(result, "Test Report")

    def test_required_input_strips_whitespace(self):
        with patch("builtins.input", return_value="  HUMINT Report  "):
            result = get_required_input("Title: ")

        self.assertEqual(result, "HUMINT Report")

    def test_valid_date_accepts_correct_format(self):
        with patch("builtins.input", return_value="2026-09-18"):
            result = get_valid_date("Date: ")

        self.assertEqual(result, "2026-09-18")

    def test_valid_date_rejects_invalid_then_accepts_valid(self):
        with patch(
            "builtins.input",
            side_effect=["09/18/2026", "2026-09-18"]
        ):
            result = get_valid_date("Date: ")

        self.assertEqual(result, "2026-09-18")

    def test_classification_selection(self):
        with patch("builtins.input", return_value="4"):
            result = get_classification()

        self.assertEqual(result, "SECRET")

    def test_discipline_selection(self):
        with patch("builtins.input", return_value="1"):
            result = get_discipline()

        self.assertEqual(result, "HUMINT")

    def test_reliability_converts_lowercase_to_uppercase(self):
        with patch("builtins.input", return_value="b"):
            result = get_reliability()

        self.assertEqual(result, "B")

    def test_credibility_selection(self):
        with patch("builtins.input", return_value="2"):
            result = get_credibility()

        self.assertEqual(result, "2")

    def test_reliability_description(self):
        result = reliability_description("B")

        self.assertEqual(result, "Usually Reliable")

    def test_credibility_description(self):
        result = credibility_description("2")

        self.assertEqual(result, "Probably True")


if __name__ == "__main__":
    unittest.main()