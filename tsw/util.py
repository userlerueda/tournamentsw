"""Utility module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


import re
from urllib.parse import parse_qs, urlparse

import daiquiri
from dateutil.parser import parse

LOGGER = daiquiri.getLogger(__name__)


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


def get_score(tsw_score: list) -> str:
    """Get formatted score."""
    LOGGER.debug("Converting TSW score '%s", tsw_score)
    score_array = []
    for set_score in tsw_score.findAll("span", recursive=False):
        score_array.append(dashed_score_to_score(set_score.contents[0]))
    return score_array


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
