import unittest
from responses import statement_helper, get_open_places, read_menu


class TestResponses(unittest.TestCase):

    def test_statement_helper_single(self):
        all_places = ["Tim Hortons"]
        statement = statement_helper(all_places, "North Campus")
        self.assertEqual(
            statement, "The only food place open in North Campus is Tim Hortons. Can I help you with something else?")

    def test_statement_helper_none(self):
        all_places = []
        statement = statement_helper(all_places, "North Campus")
        self.assertEqual(
            statement, "There are no food places open in North Campus! Can I help you with something else?")

    def test_menu_read_items(self):
        time = "breakfast"
        place = "C3"
        menu = ["Egg", "Bread", "Fruits"]
        menu_output = read_menu(menu, place, time)
        self.assertEqual(
            menu_output, "The breakfast menu for C3 is Egg, Bread, Fruits")

    def test_menu_read_multiple(self):
        place = "C3"
        menu = {"breakfast": ["Egg", "Bread", "Fruits"],
                "dinner": ["rice", "tacos", "beef"]}
        menu_output = read_menu(menu, place)
        self.assertEqual(
            menu_output, "The menu for C3 is...breakfast menu...Egg, Bread, Fruits. dinner menu...rice, tacos, beef. ")

    def test_menu_read_closed(self):
        place = "ABP"
        menu = "Closed"
        menu_output = read_menu(menu, place)
        self.assertEqual(menu_output, "ABP is Closed! ")
