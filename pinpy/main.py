from typing import List, Literal, Optional
import requests
from . import endpoints, utils
from .objects import Board, Pin, Results
import dill


class Client:
    def __init__(
        self,
        email: str = None,
        password: str = None,
        session: str | requests.Session = None,
        user_agent: str = None,
    ) -> None:
        self.email: str = email
        self.password: str = password
        self.user_id: int = None
        if type(session) == str:
            session = utils.load_session(session)
        else:
            self.session: requests.Session = session or requests.sessions.session()

            if session and not user_agent:
                user_agent = session.headers["User-Agent"]
            else:
                user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0"
            self.session.headers["User-Agent"] = user_agent

            if self.email and self.password:
                self.login(email, password)

    def save_session(self, filename) -> None:
        """Saves the current session to a file."""
        with open(filename, "wb") as f:
            dill.dump(self.session, f)

    def download_pin(
        self, pin: Pin | int | str, filename: str = "", dir_filepath: str = ""
    ) -> str:
        return utils.download_pin(pin, filename, dir_filepath, self.session)

    def download_board(
        self, board: Board, dir_filepath: str = "", amount: int = 0
    ) -> List[str]:
        if amount == 0:
            amount = len(board)
        return [
            self.download_pin(pin, dir_filepath=dir_filepath) for pin in board[:amount]
        ]

    def download_results(
        self, results: Results, dir_filepath: str = "", amount: int = 0
    ) -> List[str]:
        if amount == 0:
            amount = len(results)
        return [
            self.download_board(result, dir_filepath)
            if type(result) == Board
            else self.download_pin(result, dir_filepath=dir_filepath)
            for result in results[:amount]
        ]

    def next_results_page(self, results: Results) -> Optional[Results]:
        if results._next_bookmark == "-end-":
            return None
        return self.search(results._query, results._scope, results._next_bookmark)

    def login(self, email: str, password: str) -> requests.Response:
        """Logs into Pinterest using the default email/username option"""
        return utils.make_request(self.session, endpoints.Login, email, password)

    def get_homefeed(self, bookmark: str = "") -> Results:
        """Refreshes the authenticated user's homefeed and returns a list of pins."""
        response = utils.make_request(self.session, endpoints.GetHomefeed).json()
        pins = utils.get_resources(response, self.session)
        next_bookmark = response["resource"]["options"]["bookmarks"][0]
        warnings = response["resource_response"]["data"]["nag"]
        return Results("", "", pins, warnings, bookmark, next_bookmark)

    def search(
        self,
        query: str,
        scope: Literal["pins", "videos", "boards"] = "pins",
        bookmark: str = "",
    ) -> Results:
        """Searches Pinterest and returns a list of pins."""
        response = utils.make_request(
            self.session, endpoints.Search, query, scope, bookmark
        ).json()
        pins = utils.get_resources(response, self.session)
        next_bookmark = response["resource"]["options"]["bookmarks"][0]
        warnings = response["resource_response"]["data"]["nag"]
        return Results(query, scope, pins, warnings, bookmark, next_bookmark)
