import unittest
from menu import get_menu
dining_centers = ['center-C3',
                  'center-mainstreetmarketdiningcen', 'center-governors']


class TestMenu(unittest.TestCase):
    def test_menu_closed(self):
        date = "2019-12-16"
        menu = get_menu(dining_centers[2], date, "breakfast")
        self.assertEqual(menu, "Closed")

    def test_menu_c3_breakfast_count(self):
        date = "2020-02-04"
        menu = get_menu(dining_centers[0], date, "breakfast")
        menu_length = len(menu)
        self.assertEqual(menu_length, 13)

    def test_menu_c3_breakfast_item(self):
        date = "2020-02-04"
        menu = get_menu(dining_centers[0], date, "breakfast")
        self.assertIn("French Toast", menu)

    def test_menu_govs_dinner_count(self):
        date = "2020-02-09"
        menu = get_menu(dining_centers[2], date, "dinner")
        menu_count = len(menu)
        self.assertEquals(menu_count, 19)

    def test_menu_south_brunch_count(self):
        date = "2020-02-09"
        menu = get_menu(dining_centers[1], date, "brunch")
        menu_count = len(menu)
        self.assertEquals(menu_count, 18)
