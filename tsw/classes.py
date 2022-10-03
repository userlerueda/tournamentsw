"""TSW module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

import re
import sys
from collections import OrderedDict
from typing import Collection, Dict, List

import daiquiri
import pandas as pd
import requests
from bs4 import BeautifulSoup

from tsw.settings import Settings
from tsw.util import (
    calculate_match_date,
    clean_fixtures,
    clean_name,
    get_country,
    get_fixtures_for_draw,
    get_parameters,
    get_score,
    is_score,
    remove_seeds_from_name,
)

LOGGER = daiquiri.getLogger(__name__)


class TSW(object):
    """A class to represent a Tournament Software object."""

    def __init__(self) -> None:
        """Initialize the TSW object."""
        self.url = Settings().dict().get("url")
        cookie_url = Settings().dict().get("cookie_url")
        self.session = requests.Session()
        params = {
            "ReturnUrl": "",
            "SettingsOpen": "false",
            "CookiePurposes": 4,
            "CookiePurposes": 16,
        }
        self.session.post(cookie_url, params=params)

    def get_all_matches(
        self,
        tournament_id: str,
        draw_types: List = ["Elimination"],
        include_country: bool = False,
    ) -> Dict:
        """Get All Matches for a Tournament."""

        all_matches = []
        events = self.get_events(tournament_id)
        for event in events:
            draws = self.get_draws(tournament_id, event["id"])
            for draw in draws:
                if draw["Type"] in draw_types:
                    matches = self.get_matches(tournament_id, draw["id"])
                    for match in matches:
                        ordered_match = OrderedDict()
                        ordered_match["Category"] = event["Name"]
                        ordered_match["Timestamp"] = match["Timestamp"]
                        ordered_match["Winner Name"] = match["Winner Name"]
                        if include_country:
                            ordered_match["Winner Country"] = match[
                                "Winner Country"
                            ]
                        ordered_match["Loser Name"] = match["Loser Name"]
                        if include_country:
                            ordered_match["Loser Country"] = match[
                                "Loser Country"
                            ]
                        ordered_match["Score"] = match["Score"]

                        all_matches.append(ordered_match)
        return all_matches

    def get_matches(self, tournament_id: str, draw_id: int) -> Dict:
        """Get Matches for a Draw of an Event."""
        uri = f"/sport/drawmatches.aspx"
        url = f"{self.url}{uri}"
        params = {
            "id": tournament_id,
            "draw": draw_id,
        }
        LOGGER.debug("Using URL: %s", url)
        response = self.session.get(url, params=params)
        response.raise_for_status()
        draw_details = {}

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        df = pd.DataFrame(
            {
                "Timestamp": [],
                "Winner Country": [],
                "Winner Name": [],
                "Loser Country": [],
                "Loser Name": [],
                "Score": [],
            }
        )

        # Body
        body = table.tbody.extract()
        for tr in body.findAll("tr", recursive=False):
            row = []
            timestamp = None
            winner_name = None
            winner_country = None
            loser_name = None
            loser_country = None
            score = None
            table_count = 0
            for td in tr.findAll("td", recursive=False):
                if "plannedtime" in td.get("class", []):
                    # Date
                    date = td.contents[0].strip()
                    time = td.contents[1].contents[0].strip()
                    timestamp = f"{date} {time}"
                elif td.find("span", class_="score", recursive=False):
                    score = get_score(
                        td.find("span", class_="score", recursive=False)
                    )
                elif td.find("table", recursive=False):
                    if table_count == 0:
                        # Winner
                        winner_name = remove_seeds_from_name(
                            td.table.tr.find(
                                "a", href=re.compile(r"^player.aspx.*$")
                            )
                            .contents[0]
                            .strip()
                        )
                        winner_country = get_country(
                            td.table.tr.find(
                                "span", class_="printonly flag"
                            ).contents[0]
                        )
                    elif table_count == 1:
                        # Loser
                        loser_name = remove_seeds_from_name(
                            td.table.tr.find(
                                "a", href=re.compile(r"^player.aspx.*$")
                            )
                            .contents[0]
                            .strip()
                        )
                        loser_country = get_country(
                            td.table.tr.find(
                                "span", class_="printonly flag"
                            ).contents[0]
                        )

                    table_count += 1
                else:
                    pass
            if timestamp is None:
                if draw_details == {}:
                    draw_details = self.get_draw(tournament_id, draw_id)
                timestamp = calculate_match_date(
                    {
                        "winner": winner_name,
                        "loser": loser_name,
                        "score": score,
                        "draw_details": draw_details,
                    }
                )

            row = [
                timestamp,
                winner_country,
                winner_name,
                loser_country,
                loser_name,
                score,
            ]
            df.loc[len(df.index)] = row

        return df.to_dict("records")

    def get_draw(self, tournament_id: str, draw_id: int) -> Collection:
        """Get draw details."""
        uri = f"/sport/tournament/draw"
        url = f"{self.url}{uri}"
        params = {"id": tournament_id, "draw": draw_id}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        draw_div = soup.find("div", class_="draw")
        df = pd.read_html(draw_div.prettify())[0]
        fixtures = clean_fixtures(get_fixtures_for_draw(df))
        dates = self.get_tournament_dates(tournament_id)
        for round_name in list(fixtures.keys()):
            fixtures[round_name]["date"] = dates[round_name]["date"]
        return fixtures

    def get_draws(self, tournament_id: str, event_id: int) -> dict:
        """Get Draws for an Event in Tournament."""
        uri = f"/sport/event.aspx"
        url = f"{self.url}{uri}"
        params = {"id": tournament_id, "event": event_id}
        LOGGER.debug("Using URL: %s", url)
        response = self.session.get(url, params=params)
        response.raise_for_status()

        dfs = pd.read_html(response.text)
        df = dfs[0]
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        draws = []
        for tr in table.findAll("tr"):
            trs = tr.findAll("td")
            for each in trs:
                try:
                    link = each.find("a")["href"]
                    params = get_parameters(link)
                    draw_id = params["draw"][0]
                    draws.append(draw_id)
                except:
                    pass

        df["id"] = draws
        col_order = [
            "id",
            "Draw",
            "Size",
            "Type",
            "Qualification",
            "Consolation",
        ]
        df = df[col_order]
        return df.to_dict("records")

    def get_events(self, tournament_id: str) -> Dict:
        """Get Events for Tournament."""
        uri = f"/sport/events.aspx"
        url = f"{self.url}{uri}"
        params = {
            "id": tournament_id,
        }
        LOGGER.debug("Using URL: %s", url)
        response = self.session.get(url, params=params)
        response.raise_for_status()

        dfs = pd.read_html(response.text)
        df = dfs[0]
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table")

        events = []
        for tr in table.findAll("tr"):
            trs = tr.findAll("td")
            for each in trs:
                try:
                    link = each.find("a")["href"]
                    params = get_parameters(link)
                    event_id = params["event"][0]
                    events.append(event_id)
                except:
                    pass

        df["id"] = events
        col_order = ["id", "Name", "Draws", "Entries"]
        df = df[col_order]
        return df.to_dict("records")

    def get_tournament_dates(self, tournament_id: str):
        """Get tournament dates."""
        round_dates = {}
        uri = f"/tournament/{tournament_id}/Matches"
        url = f"{self.url}{uri}"
        response = self.session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        dates = soup.findAll("time")
        round = 1
        for date in dates:
            if round <= len(dates) - 3:
                round_dates[f"Round {round}"] = {"date": date["datetime"]}
            elif round == len(dates) - 2:
                round_dates["Quarter Finals"] = {"date": date["datetime"]}
            elif round == len(dates) - 1:
                round_dates["Semi Finals"] = {"date": date["datetime"]}
            elif round == len(dates):
                round_dates["Finals"] = {"date": date["datetime"]}
            round += 1
        return round_dates
