SPECIAL_FRAME_COUNT = 1
STRIKE_BONUS_ROLLS = 2
SPARE_BONUS_ROLLS = 1
MAX_BONUS_FRAMES_OFFSET = -2
CURRENT_FRAME_OFFSET = -1


class BowlingGame(object):

    def __init__(self, pins=10, frames=10, rolls_per_frame=2):
        self._PINS = pins
        self._FRAMES = frames
        self._REGULAR_FRAME_MAX_ROLLS = rolls_per_frame
        self.frames = []

        self._start_new_frame()

    def _start_new_frame(self):
        if len(self.frames) < self._FRAMES - SPECIAL_FRAME_COUNT:
            self.current_frame = Frame(self._REGULAR_FRAME_MAX_ROLLS, self._PINS)
        else:
            self.current_frame = LastFrame(self._REGULAR_FRAME_MAX_ROLLS, self._PINS)
        self.frames.append(self.current_frame)

    def roll(self, score):
        self._update_game_state()
        self.current_frame.add_roll(score)
        self._update_bonus_frames_if_applicable(score)

    def _update_game_state(self):
        if self.current_frame.is_done_rolling():
            if len(self.frames) < self._FRAMES:
                self._start_new_frame()
            else:
                raise RuntimeError("Game has already finished")

    def _update_bonus_frames_if_applicable(self, score):
        for bonus_frame in self.frames[MAX_BONUS_FRAMES_OFFSET + CURRENT_FRAME_OFFSET : CURRENT_FRAME_OFFSET]:
            if bonus_frame.is_expecting_bonus():
                bonus_frame.add_bonus_score(score)

    def current_score(self):
        total_score = 0
        for frame in self.frames:
            total_score = total_score + frame.total_score()

        return total_score


INVALID_SCORE_MSG = "Invalid score of {0}, maximum of {1} is allowed"
INVALID_TOTAL_SCORE_MSG = "Invalid score of {0}, expected up to {1} after previous roll"

class Frame(object):
    def __init__(self, max_rolls, max_pins):
        self._MAX_ROLLS = max_rolls
        self._MAX_PINS = max_pins
        self.rolls = []
        self.expected_bonus_rolls = 0
        self.bonus_score = 0

    def _validate_roll(self, score):
        if score > self._MAX_PINS:
            raise RuntimeError(INVALID_SCORE_MSG.format(score, self._MAX_PINS))
        elif score + self.rolled_score() > self._MAX_PINS:
            raise RuntimeError(INVALID_TOTAL_SCORE_MSG.format(score, self._MAX_PINS))

    def add_roll(self, score):
        self._validate_roll(score)
        self.rolls.append(score)
        if self.is_strike():
            self.expected_bonus_rolls = STRIKE_BONUS_ROLLS
        elif self.is_spare():
            self.expected_bonus_rolls = SPARE_BONUS_ROLLS

    def add_bonus_score(self, score):
        self.bonus_score = self.bonus_score + score
        self.expected_bonus_rolls = self.expected_bonus_rolls - 1

    def is_done_rolling(self):
        return len(self.rolls) >= self._MAX_ROLLS or self.rolled_score() >= self._MAX_PINS

    def is_expecting_bonus(self):
        return self.expected_bonus_rolls > 0

    def rolled_score(self):
        total_score = 0
        for roll in self.rolls:
            total_score = total_score + roll

        return total_score

    def total_score(self):
        if not self.is_done_rolling() or self.is_expecting_bonus():
            return 0

        return self.rolled_score() + self.bonus_score

    def is_strike(self):
        return len(self.rolls) == 1 and self.rolled_score() == self._MAX_PINS

    def is_spare(self):
        return len(self.rolls) > 1 and self.rolled_score() == self._MAX_PINS

class LastFrame(Frame):

    def is_done_rolling(self):
        return Frame.is_done_rolling(self) and not self.is_expecting_bonus()

    def add_roll(self, score):
        self._validate_roll(score)
        self.rolls.append(score)
        if self.is_expecting_bonus():
            self.add_bonus_score(0)
        elif self.is_strike():
            self.expected_bonus_rolls = STRIKE_BONUS_ROLLS
        elif self.is_spare():
            self.expected_bonus_rolls = SPARE_BONUS_ROLLS

    def _validate_roll(self, score):
        if not self.is_expecting_bonus():
            Frame._validate_roll(self, score)
        elif score > self._MAX_PINS:
            raise RuntimeError(INVALID_SCORE_MSG.format(score, self._MAX_PINS))
