import unittest
from location_status import generate_place_info, generate_open_area_info
AREAS = ["Ellicott / Greiner Hall", "North Campus Academic Buildings",
         "South Campus", "Governors", "Downtown"]


class TestLocationStatus(unittest.TestCase):

    def test_area_info_count(self):
        date = "2020-02-11"
        area_places = generate_open_area_info(AREAS[0], date)
        count_area_places = len(area_places)
        self.assertEqual(count_area_places, 10)

    def test_area_info_none_open(self):
        date = "2020-05-14"
        area_infos = generate_open_area_info(AREAS[1], date)
        count_area_places = len(area_infos)
        self.assertEqual(count_area_places, 0)

    def test_area_info_perks_time(self):
        date = "2020-02-11"
        area_infos = generate_open_area_info(AREAS[0], date)
        timing = area_infos["Perks"]
        self.assertEqual(timing, "08:00am - 12:00am")

    def test_place_info_open(self):
        date = "2020-02-11"
        timing = generate_place_info("Bert's", date)
        self.assertEqual(timing, "08:00am - 04:00pm")

    def test_place_info_close(self):
        date = "2020-02-11"
        timing = generate_place_info("UB Card at 1Capen", date)
        self.assertEqual(timing, "Closed")


if __name__ == '__main__':
    unittest.main()
