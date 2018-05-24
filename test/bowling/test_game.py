from bowling import game
import unittest

class TestBowling(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_can_roll(self):
        expected_score = 0
        game_under_test = game.BowlingGame()
        game_under_test.roll(5)
        self.assertEquals(game_under_test.current_score(), expected_score)

    def test_can_make_multiple_rolls(self):
        expected_score = 9
        game_under_test = self._regular_game_helper([7, 2, 7])
        self.assertEquals(game_under_test.current_score(), expected_score)

    def test_rolls_belong_to_frames(self):
        expected_score = 19
        expected_frame_count = 3
        game_under_test = self._regular_game_helper([1, 2, 3, 4, 5, 4])
        self.assertEquals(game_under_test.current_score(), expected_score)
        self.assertEquals(len(game_under_test.frames), expected_frame_count)

    def test_one_strike_per_frame(self):
        expected_frame_count = 3
        game_under_test = self._regular_game_helper([10, 10, 10])
        self.assertEquals(len(game_under_test.frames), expected_frame_count)

    def test_scoring_for_strike(self):
        expected_frame_count = 2
        expected_score = 14
        game_under_test = self._regular_game_helper([10, 1, 1])
        self.assertEquals(len(game_under_test.frames), expected_frame_count)
        self.assertEquals(game_under_test.current_score(), expected_score)

    def test_scoring_for_spare(self):
        expected_frame_count = 2
        expected_score = 19
        game_under_test = self._regular_game_helper([5, 5, 4, 1])
        self.assertEquals(len(game_under_test.frames), expected_frame_count)
        self.assertEquals(game_under_test.current_score(), expected_score)

    def test_can_detect_invalid_score(self):
        game_under_test = game.BowlingGame()
        try:
            game_under_test.roll(11)
            self.fail("game accepted invalid roll")
        except RuntimeError:
            pass

    def test_max_score(self):
        """
        max score test taken from code dojo recommended tests
        :return: 
        """
        expected_score = 300
        expected_frames = 10
        game_under_test = self._regular_game_helper([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])
        self.assertEquals(game_under_test.current_score(), expected_score)
        self.assertEquals(len(game_under_test.frames), expected_frames)

    def test_nine_miss_score(self):
        """
        max score test taken from code dojo recommended tests
        :return: 
        """
        expected_score = 90
        expected_frames = 10
        game_under_test = self._regular_game_helper([9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0])
        self.assertEquals(game_under_test.current_score(), expected_score)
        self.assertEquals(len(game_under_test.frames), expected_frames)

    def _regular_game_helper(self, rolls):
        game_under_test = game.BowlingGame()
        for score in rolls:
            game_under_test.roll(score)

        return game_under_test

# def test_last_bonus_scoring(self):
    #     expected_frame_count = 2
    #     expected_score = 19
    #     game_under_test = game.BowlingGame(frames=2)
    #     game_under_test.roll(10)
    #     game_under_test.roll(10)
    #     game_under_test.roll(10)
    #     game_under_test.roll(10)
    #     self.assertEquals(len(game_under_test.frames), expected_frame_count)
    #     self.assertEquals(game_under_test.current_score(), expected_score)

class TestFrame(unittest.TestCase):

    def test_can_create_frame(self):
        frame_under_test = game.Frame(2, 10)
        self.assertIsNotNone(frame_under_test)

    def test_can_add_rolls(self):
        frame_under_test = game.Frame(2, 10)
        self.assertIsNotNone(frame_under_test)
        frame_under_test.add_roll(4)
        self.assertEquals(len(frame_under_test.rolls), 1)
        frame_under_test.add_roll(5)
        self.assertEquals(len(frame_under_test.rolls), 2)

    def test_can_keep_score(self):
        frame_under_test = game.Frame(2, 10)
        self.assertIsNotNone(frame_under_test)

        frame_under_test.add_roll(4)
        self.assertFalse(frame_under_test.is_done_rolling())
        self.assertEquals(frame_under_test.total_score(), 0)

        frame_under_test.add_roll(5)
        self.assertTrue(frame_under_test.is_done_rolling())
        self.assertEquals(frame_under_test.total_score(), 9)

    def test_can_keep_spare_score(self):
        frame_under_test = game.Frame(2, 10)
        self.assertIsNotNone(frame_under_test)

        frame_under_test.add_roll(4)
        self.assertFalse(frame_under_test.is_done_rolling())
        self.assertFalse(frame_under_test.is_expecting_bonus())
        self.assertEquals(frame_under_test.total_score(), 0)

        frame_under_test.add_roll(6)
        self.assertTrue(frame_under_test.is_done_rolling())
        self.assertTrue(frame_under_test.is_expecting_bonus())
        self.assertEquals(frame_under_test.total_score(), 0)

        frame_under_test.add_bonus_score(5)
        self.assertTrue(frame_under_test.is_done_rolling())
        self.assertFalse(frame_under_test.is_expecting_bonus())
        self.assertEquals(frame_under_test.total_score(), 15)

    def test_can_keep_spare_score(self):
        frame_under_test = game.Frame(2, 10)
        self.assertIsNotNone(frame_under_test)

        frame_under_test.add_roll(10)
        self.assertTrue(frame_under_test.is_done_rolling())
        self.assertTrue(frame_under_test.is_expecting_bonus())
        self.assertEquals(frame_under_test.total_score(), 0)

        frame_under_test.add_bonus_score(5)
        self.assertTrue(frame_under_test.is_done_rolling())
        self.assertTrue(frame_under_test.is_expecting_bonus())
        self.assertEquals(frame_under_test.total_score(), 0)

        frame_under_test.add_bonus_score(5)
        self.assertTrue(frame_under_test.is_done_rolling())
        self.assertFalse(frame_under_test.is_expecting_bonus())
        self.assertEquals(frame_under_test.total_score(), 20)

    def test_will_reject_invalid_roll(self):
        frame_under_test = game.Frame(2, 10)
        self.assertIsNotNone(frame_under_test)

        try:
            frame_under_test.add_roll(11)
            self.fail("accepted invalid roll")
        except RuntimeError:
            pass

    def test_will_reject_invalid_second_roll(self):
        frame_under_test = game.Frame(2, 10)
        self.assertIsNotNone(frame_under_test)

        try:
            frame_under_test.add_roll(6)
        except RuntimeError:
            self.fail("accepted invalid roll")

        try:
            frame_under_test.add_roll(6)
            self.fail("accepted invalid roll")
        except RuntimeError:
            pass
