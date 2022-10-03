"""Utility module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


import re
from typing import Collection, Dict
from urllib.parse import parse_qs, urlparse

import daiquiri
from dateutil.parser import parse

LOGGER = daiquiri.getLogger(__name__)


def calculate_match_date(match_details: Dict) -> str:
    """Calculate match date."""
    match_date = None
    LOGGER.debug("Calculating match date for '%s'", match_details)
    draw_details = match_details.get("draw_details", {})
    winner = match_details.get("winner")
    loser = match_details.get("loser")
    for round_name in list(draw_details.keys()):
        for match in draw_details[round_name]["matches"]:
            if winner and winner in match and loser and loser in match:
                match_date = draw_details[round_name].get("date")
                break
    return match_date


def get_parameters(url: str) -> dict:
    """Get parameters from a URL."""
    parse_result = urlparse(url)
    dict_result = parse_qs(parse_result.query)
    return dict_result


def get_country(tsw_country: str) -> str:
    """Get Three letter country name."""
    countries = re.findall(r"\[([A-Z]{3})\]", tsw_country)
    if len(countries) == 1:
        return countries[0]
    else:
        return ""


def get_fixtures_for_draw(draw) -> Collection:
    """Get fixtures for draw"""
    fixtures = {}
    round_size = 0
    for column_name in draw.columns:
        if "Round" in column_name or "Finals" in column_name:
            column = list(draw[column_name])
            if round_size != 0 and round_size != len(column):
                LOGGER.warning("Found draw with inconsistent columns...")
            else:
                round_size = len(column)
            fixtures[column_name] = [clean_name(element) for element in column]
    return fixtures


def clean_fixtures(fixtures: Dict) -> Dict:
    """Clean fixtures."""
    number_of_rounds = len(fixtures.items())
    new_fixtures = {}
    for round_number in range(number_of_rounds):
        round_name = list(fixtures.keys())[round_number]
        new_fixtures[round_name] = {"matches": []}
        fixture = []
        player = 1
        for element in range(
            pow(2, round_number),
            pow(2, number_of_rounds + 1),
            pow(2, round_number + 1),
        ):
            fixture.append(fixtures[round_name][element])
            if player == 2:
                new_fixtures[round_name]["matches"].append(fixture)
                fixture = []
                player = 0
            player += 1

    return new_fixtures


def get_score(tsw_score: list) -> str:
    """Get formatted score."""
    LOGGER.debug("Converting TSW score '%s", tsw_score)
    score_array = []
    if tsw_score.findAll("span", recursive=False):
        for set_score in tsw_score.findAll("span", recursive=False):
            score_array.append(dashed_score_to_score(set_score.contents[0]))
    else:
        score_array = tsw_score.contents
    return score_array


def is_score(string: str) -> bool:
    """Check if string is a score."""
    LOGGER.info("Checking to see if '%s' is a score", string)
    regular_set_score = r"\d+\-\d+"
    if re.match(regular_set_score, str(string)):
        return True
    return False


def dashed_score_to_score(dashed_score: str) -> str:
    """Convert dashed score to score."""
    LOGGER.debug("Converting dashed score '%s", dashed_score)
    score = []
    set_regex = r"(\d+)\s*\-\s*(\d+)"
    set_score = score = re.findall(set_regex, dashed_score)
    score = list(sum(set_score, ()))
    tiebreak_regex = r"\(\s*(\d+)\s*\)"
    tiebreak_score = re.findall(tiebreak_regex, dashed_score)
    if len(tiebreak_score) == 1:
        score.append(int(tiebreak_score[0]))
    score = [int(result) for result in score]
    return score


def clean_name(dirty_name: str) -> str:
    """Clean name."""

    LOGGER.debug("Cleaning name '%s", dirty_name)

    # Remove [5/8]
    name = re.sub(r"\[\d\/\d\]", "", str(dirty_name))

    # Remove [1]
    name = re.sub(r"\[\d\]", "", name)

    # Remove [COL]
    name = re.sub(r"\[[A-Z]+\]", "", name)

    # Remove whitespace at the begining
    name = re.sub(r"^\s+", "", name)

    # Remove whitespace at the end
    name = re.sub(r"\s+$", "", name)

    return name


def remove_seeds_from_name(name_with_seed: str) -> str:
    """Remove seeds from name."""

    LOGGER.debug("Removing seeds for name '%s", name_with_seed)

    # Remove [5/8]
    name = re.sub(r"\[\d\/\d]", "", name_with_seed)

    # Remove [1]
    name = re.sub(r"\[\d\]", "", name)

    # Remove whitespace at the end
    name = re.sub(r"\s+$", "", name)
    return name
