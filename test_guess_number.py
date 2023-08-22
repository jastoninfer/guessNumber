"""
This is an unittest module for GuessNumber.
"""

import unittest
from unittest.mock import patch
from guess_number import GuessNumber


class MyTestCase(unittest.TestCase):
    """
    This is a class containing methods to test guess_number.
    """
    guessNumber = GuessNumber()

    def test_check_format(self):
        """ This tests if check_format accepts and only
        accepts 4-digit numbers """
        self.assertTrue(self.guessNumber.check_format('1234'))
        self.assertFalse(self.guessNumber.check_format('123'))
        self.assertFalse(self.guessNumber.check_format('0123'))
        self.assertFalse(self.guessNumber.check_format('54123'))
        self.assertFalse(self.guessNumber.check_format(''))
        with self.assertRaises(TypeError):
            self.guessNumber.check_format(1234)
        self.assertTrue(self.guessNumber.check_format('9999'))
        self.assertTrue(self.guessNumber.check_format('1000'))
        self.assertFalse(self.guessNumber.check_format('12 3'))

    def test_check_value(self):
        """ This checks given num against the randomly generated target,
        and returns the correct hints per the requirement"""
        self.assertEqual('oooo', self.guessNumber.check_value('1234', '1234'))
        self.assertEqual('xxxx', self.guessNumber.check_value('4321', '1234'))
        self.assertEqual('xoox', self.guessNumber.check_value('4231', '1234'))
        self.assertEqual('##ox', self.guessNumber.check_value('9831', '1234'))
        self.assertEqual('oxxx', self.guessNumber.check_value('1111', '1234'))

    def test_check_quit(self):
        """ This checks if the user can quit according to the guide """
        self.assertTrue(self.guessNumber.check_quit('q'))
        self.assertTrue(self.guessNumber.check_quit('Q'))
        self.assertFalse(self.guessNumber.check_quit('qx'))
        self.assertFalse(self.guessNumber.check_quit(''))

    def test_check_replay(self):
        """ This checks if the user can replay according to the guide """
        self.assertTrue(self.guessNumber.check_replay('r'))
        self.assertTrue(self.guessNumber.check_replay('R'))
        self.assertFalse(self.guessNumber.check_replay('$sd'))
        self.assertFalse(self.guessNumber.check_replay(''))

    def test_move_forward(self):
        """ This checks if the game can be properly finished and steps
        can be accumulated"""
        prev = self.guessNumber.num_attempts
        self.assertFalse(self.guessNumber.move_forward('oooo'))
        # should finish and return False
        self.assertEqual(1 + prev, self.guessNumber.num_attempts)

        prev = self.guessNumber.num_attempts
        self.assertTrue(self.guessNumber.move_forward('####'))
        # should not finish and return True
        self.assertEqual(1 + prev, self.guessNumber.num_attempts)

        prev = self.guessNumber.num_attempts
        self.assertTrue(self.guessNumber.move_forward('#x#o'))
        # should not finish and return True
        self.assertEqual(1 + prev, self.guessNumber.num_attempts)

    def test_reset(self):
        """ This checks if the game can be properly reset"""
        prev = self.guessNumber.target
        self.guessNumber.reset()
        self.assertEqual(0, self.guessNumber.num_attempts)
        self.assertNotEqual(prev, self.guessNumber.target)

        prev = self.guessNumber.target
        self.guessNumber.reset()
        self.assertEqual(0, self.guessNumber.num_attempts)
        self.assertNotEqual(prev, self.guessNumber.target)

    @patch('builtins.input', side_effect=['9876', 'q', '1234', '467',
                                          '5320', '$#s', '1237', 'Q'])
    def test_get_input(self, mock_input):  # pylint: disable = unused-argument
        """ This checks if the game can continually ask for a 4-digit number"""
        self.assertEqual('9876', self.guessNumber.get_input())
        self.assertIsNone(self.guessNumber.get_input())
        self.assertEqual('1234', self.guessNumber.get_input())
        self.assertEqual('5320', self.guessNumber.get_input())
        self.assertEqual('1237', self.guessNumber.get_input())
        self.assertIsNone(self.guessNumber.get_input())

    @patch('builtins.input', side_effect=['9831', '3479', '1234', 'R',
                                          '9831', 'q', '1239', 'q',
                                          '1234', 'Q'])
    def test_run(self, mock_input):  # pylint: disable = unused-argument
        """ This checks if the game can record how many attempts used
        and if re-play after finish and exit midway are supported"""
        self.guessNumber.history = []
        self.guessNumber.target = '1234'
        self.guessNumber.run()
        self.assertEqual(self.guessNumber.history, [3])

        self.guessNumber.history = []
        self.guessNumber.target = '1234'
        self.guessNumber.run()
        self.assertEqual(self.guessNumber.history, [])

        print(self.guessNumber.num_attempts)
        self.guessNumber.history = []
        self.guessNumber.target = '1234'
        self.guessNumber.run()
        self.assertEqual(self.guessNumber.history, [1])


if __name__ == '__main__':
    unittest.main()
