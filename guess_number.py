"""
This a file containing class GuessNumber and entrance function to run the game.
"""
import random


class GuessNumber:
    """
    Our 4-digit number guessing game is defined here. Note run() is where
    you can start a new game.
    """
    def __init__(self):
        self.num_digits = 4  # because we are guessing a 4-digit number
        self.sym = {'match': 'o', 'found': 'x', 'not_found': '#'}
        self.symbols = {'quit': ['q', 'Q'], 'replay': ['r', 'R']}
        self.target = str(random.randint(1000, 9999))
        self.num_attempts = 0
        self.history = []
        # a list num, num of attempts tried to successfully guess the target
        self.msg = {}  # initialize to an empty dict, use setup_message to fill
        self.setup_message()

    def setup_message(self):
        """
        Messages and prompts required while interacting are stored in self.msg.
        :return:
        """
        prompt_quit = ' or '.join(self.symbols['quit'])
        prompt_replay = ' or '.join(self.symbols['replay'])
        self.msg = {'quiting': 'Quiting for you.',
                    'incorrect_format': 'Incorrect input format.',
                    'hint': 'Hint for this input: {}',
                    'prompt_next_number': f'Please input a number to continue '
                                          f'or input {prompt_quit} to quit',
                    'prompt_replay': f'Congratulations. '
                                     f'Your guess is right. Totally {{}} '
                                     f'steps taken. Input {prompt_replay}'
                                     f' to re-play,'
                                     f' or input any other key to quit.'
                    }

    def check_replay(self, symbol):
        """
        This function compares input symbol with self.REPLAY_SYMBOL
        :param symbol: input string
        :return: True if matches otherwise False
        """
        return symbol in self.symbols['replay']

    def check_quit(self, symbol):
        """
        This function compares input symbol with self.QUIT_SYMBOL
        :param symbol: input string
        :return: True if matches otherwise False
        """
        return symbol in self.symbols['quit']

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
        if len(num) == self.num_digits and num.isdigit() and num[0] != '0':
            return True
        return False

    def check_value(self, num, target=None):
        """
        This function checks to what extent num is matched to target and return
        an appropriate hint on each digit. Note check_format should be
        called before this function.
        :param num: input number to be checked
        :param target: number to be compared with, default is self.TARGET.
        :return: a hint of 4 characters where 'o' is matched on spot,
        'x' is digit placed on the wrong spot, '#' is wrong digit.
        """
        if target is None:
            target = self.target
        hint = ''.join(map(lambda x, y: self.sym['match'] if x == y else (
            self.sym['found'] if x in list(target) else
            self.sym['not_found']), num, target))
        return hint

    def move_forward(self, hint):
        """
        This function is used to properly update the state of this class
        after a given input is verified. If hint equals 'oooo', we need to
        finish this game, otherwise, move to the next step, fetch some
        new guess. In both cases, increase num_attempts by 1.
        :param hint: hint calculated from user input
        :return: False if we should finish, otherwise True.
        """
        self.num_attempts += 1
        return not all(c == self.sym['match'] for c in hint)

    def reset(self):
        """
        This function reset the game, i.e., set num_attempts to 0
        and renew the target But history will be kept
        :return:
        """
        self.num_attempts = 0
        self.target = str(random.randint(1000, 9999))

    def get_input(self):
        """
        This function will keep asking the user for a valid
        input until the user choose to exit or has input a valid
        4-digit number.
        :return: None if user exit, otherwise the valid
        4-digit number in string format
        """
        while True:
            print(self.msg['prompt_next_number'])
            token = input()
            if self.check_quit(token):
                print(self.msg['quiting'])
                return None
            if not self.check_format(token):
                print(self.msg['incorrect_format'])
                continue
            return token

    def run(self):
        """
        This function is the entrance to playing a new game.
        :return:
        """
        while True:
            token = self.get_input()
            if token is None:
                # upon exit, clear steps made
                self.reset()
                break
            hint = self.check_value(token)
            print(self.msg['hint'].format(hint))
            if not self.move_forward(hint):
                print(self.msg['prompt_replay'].format(self.num_attempts))
                # upon success, push current num of attempts to history
                # and clear steps made
                self.history.append(self.num_attempts)
                self.reset()
                if not self.check_replay(input()):
                    break


if __name__ == '__main__':
    guessNumber = GuessNumber()
    guessNumber.run()
