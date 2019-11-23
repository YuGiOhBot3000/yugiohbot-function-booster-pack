import unittest

import main


class TestMain(unittest.TestCase):
    def test_get_top_reactions(self):
        mock_reactions = [
            {'id': '123', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '456', 'reactions': {'WOW': 1, 'HAHA': 1}, 'total': 2},
            {'id': '789', 'reactions': {'WOW': 1, 'HAHA': 4}, 'total': 5},
            {'id': '135', 'reactions': {'WOW': 10, 'HAHA': 100}, 'total': 110},
            {'id': '246', 'reactions': {'WOW': 10, 'HAHA': 11}, 'total': 21}
        ]
        expected = [
            {'id': '135', 'reactions': {'WOW': 10, 'HAHA': 100}, 'total': 110},
            {'id': '246', 'reactions': {'WOW': 10, 'HAHA': 11}, 'total': 21},
            {'id': '123', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '789', 'reactions': {'WOW': 1, 'HAHA': 4}, 'total': 5}
        ]
        threshold = 5
        result = main.get_top_reactions(mock_reactions, threshold)
        self.assertEqual(result, expected)

    def test_create_booster_pack_less_than_9(self):
        reactions = [
            {'id': '135', 'reactions': {'WOW': 10, 'HAHA': 100}, 'total': 110},
            {'id': '246', 'reactions': {'WOW': 10, 'HAHA': 11}, 'total': 21},
            {'id': '123', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '124', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '125', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '126', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '789', 'reactions': {'WOW': 1, 'HAHA': 4}, 'total': 5}
        ]
        result = main.create_booster_pack(reactions)
        self.assertTrue(len(result) == 5)

    def test_create_booster_pack_more_than_9(self):
        reactions = [
            {'id': '135', 'reactions': {'WOW': 10, 'HAHA': 100}, 'total': 110},
            {'id': '246', 'reactions': {'WOW': 10, 'HAHA': 11}, 'total': 21},
            {'id': '123', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '124', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '125', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '126', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '789', 'reactions': {'WOW': 1, 'HAHA': 4}, 'total': 5},
            {'id': '125', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '126', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '789', 'reactions': {'WOW': 1, 'HAHA': 4}, 'total': 5}
        ]
        result = main.create_booster_pack(reactions)
        self.assertTrue(len(result) == 9)

    def test_create_booster_pack_less_than_5(self):
        reactions = [
            {'id': '135', 'reactions': {'WOW': 10, 'HAHA': 100}, 'total': 110},
            {'id': '246', 'reactions': {'WOW': 10, 'HAHA': 11}, 'total': 21},
            {'id': '123', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20},
            {'id': '124', 'reactions': {'WOW': 10, 'HAHA': 10}, 'total': 20}
        ]
        result = main.create_booster_pack(reactions)
        self.assertTrue(len(result) == 0)


if __name__ == '__main__':
    unittest.main()
