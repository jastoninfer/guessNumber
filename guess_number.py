import random
class GuessNumber(object):
    def __init__(self):
        self.NUM_DIGITS = 4 # because we are guessing a 4-digit number
        self.SYM_MATCH = 'o' # to represent a match in the right spot
        self.SYM_FOUND = 'x' # a match in a different spot
        self.SYM_NOT_FOUND = '#' # mismatch
        self.QUIT_SYMBOLS = ['q', 'Q']
        self.REPLAY_SYMBOLS = ['r', 'R']
        self.MSG_QUITING = 'Quiting for you.'
        self.MSG_INCORRECT_FORMAT = 'Incorrect input format.'
        self.MSG_HINT = 'Hint for this input: {}'
        self.TARGET = str(random.randint(1000, 9999))
        self.num_attempts = 0
        self.PROMPT_NEXT_NUMBER = 'Please input a number to continue, or input {} to quit'.format(
            ' or '.join(self.QUIT_SYMBOLS))
        self.PROMPT_REPLAY = 'Congratulations. Your guess is right. Totally {{}} steps taken. Input {s2}' \
                             ' to re-play, or input any other key to quit.'.format(s2=' or '.join(self.REPLAY_SYMBOLS))
        self.history = [] # a list num, # attempts tried to successfully guess the target

    def check_replay(self, symbol):
        """
        This function compares input symbol with self.REPLAY_SYMBOL
        :param symbol: input string
        :return: True if matches otherwise False
        """
        return symbol in self.REPLAY_SYMBOLS

    def check_quit(self, symbol):
        """
        This function compares input symbol with self.QUIT_SYMBOL
        :param symbol: input string
        :return: True if matches otherwise False
        """
        return symbol in self.QUIT_SYMBOLS

    def check_format(self, num):
        """
        This function checks if num is a string and composed of 4-digit numbers
        with nonzero value in the first digit
        :param num: input number to be checked
        :return: True if passed else False
        """
        if not isinstance(num, str):
            raise TypeError()
        # check length, each digit, and the first digit
        if len(num) == self.NUM_DIGITS and num.isdigit() and num[0] != '0':
            return True
        return False

    def check_value(self, num, target=None):
        """
        This function checks to what extent num is matched to target and return
        an appropriate hint on each digit. Note check_format should be called before
        this function.
        :param num: input number to be checked
        :param target: number to be compared with, default is self.TARGET.
        :return: a hint of 4 characters where 'o' is matched on spot, 'x' is digit
        placed on the wrong spot, '#' is wrong digit.
        """
        if target is None:
            target = self.TARGET
        get_hint = lambda x, y: self.SYM_MATCH if x == y \
            else(self.SYM_FOUND if x in list(target) else self.SYM_NOT_FOUND)
        hint = ''.join(map(get_hint, num, target))
        return hint

    def move_forward(self, hint):
        """
        This function is used to properly update the state of this class after a given input
        is verified. If hint equals 'oooo', we need to finish this game, otherwise, move to the
        next step, fetch some new guess. In both cases, increase num_attempts by 1.
        :param hint: hint calculated from user input
        :return: False if we should finish, otherwise True.
        """
        self.num_attempts += 1
        return not all(c == self.SYM_MATCH for c in hint)

    def reset(self):
        """
        This function reset the game, i.e., set num_attempts to 0 and renew the target
        But history will be kept
        :return:
        """
        self.num_attempts = 0
        self.TARGET = str(random.randint(1000, 9999))

    def get_input(self):
        """
        This function will keep asking the user for a valid input until the user
        choose to exit or has input a valid 4-digit number.
        :return: None if user exit, otherwise the valid 4-digit number in string format
        """
        while (True):
            print(self.PROMPT_NEXT_NUMBER)
            token = input()
            if self.check_quit(token):
                print(self.MSG_QUITING)
                return None
            if not self.check_format(token):
                print(self.MSG_INCORRECT_FORMAT)
                continue
            return token

    def run(self):
        """
        This function is the entrance to playing a new game.
        :return:
        """
        while(True):
            token = self.get_input()
            if token is None:
                # upon exit, clear steps made
                self.reset()
                break
            hint = self.check_value(token)
            print(self.MSG_HINT.format(hint))
            if not self.move_forward(hint):
                print(self.PROMPT_REPLAY.format(self.num_attempts))
                # upon success, push current num of attempts to history
                # and clear steps made
                self.history.append(self.num_attempts)
                self.reset()
                if not self.check_replay(input()):
                    break

if __name__ == '__main__':
    guessNumber = GuessNumber()
    guessNumber.run()
