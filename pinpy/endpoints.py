import json


class Endpoint:
    def __init__(self) -> None:
        self.url: str
        self.method: str
        self.fresh_headers: bool = False
        self.headers: dict = {
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        if self.method == "post":
            self.json: dict = {}
            self.data: bytes | str = ""


class Login(Endpoint):
    method: str = "post"

    def __init__(self, email, password) -> None:
        self.url: str = "https://accounts.pinterest.com/v3/login/handshake/"
        super().__init__()
        self.email: str = email
        self.password: str = password
        self.data = (
            f"username_or_email={self.email}&password={self.password}&referrer=&token="
        )


class GetHomefeed(Endpoint):
    method: str = "get"

    def __init__(self, bookmark: str = "") -> None:
        super().__init__()
        self.bookmark = bookmark
        self.url: str = (
            "https://www.pinterest.com/resource/UserHomefeedResource/get/?source_url=/&data="
            + json.dumps(
                {
                    "options": {
                        "field_set_key": "hf_grid",
                        "in_nux": False,
                        "in_news_hub": False,
                        "prependPartner": False,
                        "static_feed": False,
                        "bookmarks": [self.bookmark],
                        "no_fetch_context_on_resource": False,
                    },
                    "context": {},
                }
            )
        )


class GetPin(Endpoint):
    method: str = "get"

    def __init__(self, pin_id: int | str) -> None:
        super().__init__()
        self.pin_id = pin_id
        self.url = f"https://www.pinterest.com/pin/{self.pin_id}/"


class Search(Endpoint):
    method: str = "get"

    def __init__(self, query: str, scope: str = "pins", bookmark: str = "") -> None:
        super().__init__()
        self.query = query
        self.scope = scope
        self.bookmark = bookmark
        self.url = (
            f"https://www.pinterest.com/resource/BaseSearchResource/get/?source_url=/search/pins/?q={self.query}&data="
            + json.dumps(
                {
                    "options": {
                        "query": self.query,
                        "redux_normalize_feed": True,
                        "scope": self.scope,
                        "bookmarks": [self.bookmark],
                    },
                    "context": {},
                }
            )
        )
