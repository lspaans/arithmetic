#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A kids game intended for learning arithmetic"""

import random
import re
import os
import sys

__author__ = "Léon Spaans"
__date__ = "2017-12-31"
__status__ = "Development"
__version__ = "0.1.0"

MAX_GAME_ROUNDS = 10
THRESHOLD = 10


class Exercise(object):
    """A base class for generating arithmetic exercises"""
    _operator = None
    _operator_method = None

    def __init__(self, threshold=THRESHOLD):
        self._cache = []
        self._threshold = threshold

    @property
    def cache(self):
        """
        Cache property; used for storing provided number combinations.

        Returns list() of set() of which set() has 2 int() numbers.
        """
        return self._cache

    @property
    def details(self):
        """
        Excercise property; used for providing exercise numbers and the
        corresponding result.

        Returns list() with 2 int() numbers and int() with result.
        """
        num1, num2 = self.number, self.number

        while {num1, num2} in self.cache:
            num1, num2 = self.number, self.number

        self.cache.append({num1, num2})

        if self._operator_method == "__sub__":
            if num2 > num1:
                num1, num2 = num2, num1

        return [num1, num2], str(getattr(num1, self._operator_method)(num2))

    @property
    def number(self):
        """
        Number property; used for generating random number.

        Returns int() with number.
        """
        return int(self.threshold * random.random()) + 1

    @property
    def operator(self):
        """
        Operator property; used for providing character indicating the
        exercise operation.

        Returns str() with operator.
        """
        return self._operator

    @property
    def threshold(self):
        """
        Threshold property; used for threshold of randomly generated number.

        Returns int() with threshold.
        """
        return self._threshold


class Addition(Exercise):
    """A class for generating addition exercises"""
    _operator = "+"
    _operator_method = "__add__"


class Division(Exercise):
    """A class for generating division exercises"""
    _operator = "/"

    @property
    def details(self):
        """
        Excercise property; used for providing exercise numbers and the
        corresponding result.

        Returns list() with 2 int() numbers and int() with result.
        """
        num1, num2 = self.number, self.number

        while {num1, num2} in self.cache:
            num1, num2 = self.number, self.number

        self.cache.append({num1, num2})

        return [num1 * num2, num2], str(num1)


class Multiplication(Exercise):
    """A class for generating multiplication exercises"""
    _operator = "x"
    _operator_method = "__mul__"


class Subtraction(Exercise):
    """A class for generating subtraction exercises"""
    _operator = "-"
    _operator_method = "__sub__"


def do_game_loop(max_game_rounds=MAX_GAME_ROUNDS):
    """
    Do main game loop.

    Arguments:
        max_exercises - int(): number of rounds
    """
    game_round, wrong, right = 0, 0, 0
    exercises = (
        Addition(),
        Division(),
        Subtraction(),
        Multiplication()
    )

    while game_round < max_game_rounds:
        game_round += 1
        exercise = random.choice(exercises)
        numbers, result = exercise.details
        answer = ""

        print(
            (
                "\nRonde {game_round}:\n" +
                "Wat is {num1} {operator} {num2} ?"
            ).format(
                game_round=game_round,
                num1=numbers[0],
                operator=exercise.operator,
                num2=numbers[1]
            )
        )

        while not re.match(r"^-?\d+$", answer):
            answer = input(">>> ").strip()

        if answer == str(result):
            print(get_compliment())

            right += 1
        else:
            print("{motivation} Het antwoord is {answer}.".format(
                motivation=get_motivation(),
                answer=result
            ))

            wrong += 1

        print(
            "[goed : {right}, fout: {wrong}]".format(
                right=right,
                wrong=wrong
            )
        )

    print(
        "\n{statistics}".format(
            statistics=get_statistics(right, max_game_rounds)
        )
    )


def get_compliment():
    """Returns str() with compliment."""
    return random.choice((
        "Goed zo!",
        "Netjes hoor!",
        "Heel knap!",
        "Jaaaaaaa!",
        "Bril...jant!",
        "Fantastisch!",
        "Ga zo door!",
        ":-)",
    ))


def get_motivation():
    """Returns str() with motivational text."""
    return random.choice((
        "Jammer!",
        "Blijven volhouden!",
        "Nee helaas!",
        "Dat klopt niet",
        ":-(",
        "Blehhhhhhhhhh!"
    ))


def get_script_name():
    """Returns str() with stylized script name"""
    return os.path.splitext(os.path.basename(sys.argv[0]))[0].upper()


def get_statistics(right, max_exercises):
    """
    Constructs statistics overview.

    Arguments:
        right         - int(): number correct answers
        max_exercises - int(): maximum number of made exercises

    Returns str() with overview.
    """
    pct_right = round((100 / max_exercises) * right)

    if pct_right == 100:
        return "Wat fantastisch! Je hebt ALLES goed! Gefeliciteerd Slimpie!"
    elif pct_right > 80:
        return "Supernetjes! Je hebt {right} van de {exercises} goed!".format(
            right=right,
            exercises=max_exercises
        )
    elif pct_right > 60:
        return (
            "Goed gedaan hoor! Je hebt {right} van de {exercises} goed!"
        ).format(
            right=right,
            exercises=max_exercises
        )
    elif pct_right > 40:
        return (
            "Helaas, net geen voldoende! :-( " +
            "Je hebt {right} van de {exercises} goed!"
        ).format(
            right=right,
            exercises=max_exercises
        )
    elif pct_right > 20:
        return (
            "Je hebt je best gedaan! Volgende keer beter!" +
            "Je hebt {right} van de {exercises} goed!"
        ).format(
            right=right,
            exercises=max_exercises
        )

    return "Jammer, je hebt geen van de antwoorden goed. Blijf oefenen!"


def main():
    """The main function"""
    print("Welkom bij ::{script}::".format(script=get_script_name()))

    try:
        do_game_loop()
    except (EOFError, KeyboardInterrupt):
        pass

    print("\n+++ Tot ziens! +++")


if __name__ == "__main__":
    main()
