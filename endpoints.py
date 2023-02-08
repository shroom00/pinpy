from dataclasses import dataclass


class Endpoint():
    url_needs_base: bool = False
    url: str
    method: str
    fresh_headers: bool = False
    headers: dict = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"}

    
    def __init_subclass__(self) -> None:
        if self.method == "post":
            self.json: dict = {}
            self.data: bytes | str = ""

@dataclass()
class Login(Endpoint):
    url = "https://accounts.pinterest.com/v3/login/handshake/"
    method = "post"
    email: str
    password: str
    
    def __post_init__(self) -> None:
        self.data = f"username_or_email={self.email}&password={self.password}&referrer=&token="

class GetHomefeed(Endpoint):
    url_needs_base = True
    url = '%s/resource/UserHomefeedResource/get/?source_url=/&data={"options":{"field_set_key":"hf_grid","in_nux":false,"in_news_hub":false,"prependPartner":false,"static_feed":false,"bookmarks":[""],"no_fetch_context_on_resource":false},"context":{}}'
    method = "get"
