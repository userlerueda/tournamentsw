"""Test utilty module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from unittest import TestCase

import pytest
from bs4 import BeautifulSoup

from tsw.util import (
    dashed_score_to_score,
    get_country,
    get_score,
    remove_seeds_from_name,
)


class TestUtilities:
    @pytest.mark.parametrize(
        "tsw_country, country",
        [
            ("[COL] ", "COL"),
            (" [COL] ", "COL"),
            (" [] ", ""),
            (" Invalid ", ""),
        ],
    )
    def test_valid_get_country(self, tsw_country, country):
        """
        Test valid get_country
        """

        assert country == get_country(tsw_country)

    # @pytest.mark.parametrize(
    #     "tsw_score, score",
    #     [
    #         (
    #             """<span class="score"><span>6-3</span><span>6-3</span></span>""",
    #             [[6, 3], [6, 2]],
    #         ),
    #         (
    #             """<span class="score"><span>6-0</span><span>6-0</span></span>""",
    #             [[6, 0], [6, 0]],
    #         ),
    #     ],
    # )
    # def test_valid_get_score(self, tsw_score, score):
    #     """
    #     Test valid get_score
    #     """

    #     soup = BeautifulSoup(tsw_score, "html.parser")
    #     print(soup)

    #     assert score == get_score(soup)

    @pytest.mark.parametrize(
        "dashed_score, score",
        [
            ("6-3", [6, 3]),
            ("6-3 (5)", [6, 3, 5]),
            ("10-2", [10, 2]),
            ("14-12", [14, 12]),
            ("6-7(5)", [6, 7, 5]),
        ],
    )
    def test_dashed_score_to_score(self, dashed_score, score):
        """
        Test dashed_score_to_score
        """

        assert score == dashed_score_to_score(dashed_score)

    @pytest.mark.parametrize(
        "name_with_seed, name",
        [
            ("Pedro Gutiérrez Pedro Gutiérrez [5/8]  ", "Pedro Gutiérrez"),
        ],
    )
    def test_remove_seeds_from_name(self, name_with_seed, name):
        """
        Test remove_seeds_from_name
        """

        assert name == remove_seeds_from_name(name_with_seed)
