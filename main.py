from typing import List
import requests
import endpoints
import dill
from exceptions import PinterestError
from objects import Pin


class Client():
    def __init__(self,
                 email: str | None = None,
                 password: str | None = None,
                 base_url: str | None = None,
                 session: requests.Session | None = None,
                 user_agent: str | None = None
                 ) -> None:
        self.email: str = email
        self.password: str = password
        self.base_url: str = base_url or "https://www.pinterest.co.uk"
        
        if type(session) == str:
            session = self._load_session(session)
        else:
            self.session: requests.Session = session or requests.sessions.session()
            
            if session and not user_agent:
                user_agent = session.headers["User-Agent"]
            else:
                user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0"
            self.session.headers["User-Agent"] = user_agent
            
            if self.email and self.password:
                self.login(email, password)
    
    def _make_request(self, endpoint: endpoints.Endpoint, *args, **kwargs) -> requests.Response:
        """Utility function to make a request to an endpoint and handle errors."""
        url = endpoint.url % self.base_url if endpoint.url_needs_base else endpoint.url
        e: endpoints.Endpoint = endpoint(*args, **kwargs)
        
        headers: dict = self.session.headers
        if e.fresh_headers:
            headers = e.headers
        else:
            headers.update(e.headers)
        
        if e.method == "get":
            response = self.session.get(url)
        elif e.method == "post":
            if e.data:
                response = self.session.post(url, data=e.data, headers=headers)
            else:
                response = self.session.post(url, json=e.json, headers=headers)
        
        self.session.cookies.update(response.cookies)
        self.session.headers["Cookie"] = "; ".join([f"{cookie.name}={cookie.value}" for cookie in self.session.cookies])

        if "application/json" in response.headers.get("Content-Type", ""):
            if ("error" in response.json() or ("status" in response.json() and response.json()["status"] in ["failure", 400])):
                raise PinterestError(response)
        return response

    def _load_session(self, filename) -> None:
        """Loads a session from a previous instance to avoid logging in multiple times."""
        with open(filename, "rb") as f:
            self.session = dill.load(f)
    
    def save_session(self, filename) -> None:
        """Saves the current session to a file."""
        with open(filename, "wb") as f:
            dill.dump(self.session, f)
    
    def login(self, email: str, password: str) -> requests.Response:
        """Logs into Pinterest using the default email/password option"""
        return self._make_request(endpoints.Login, email, password)
    
    def get_homefeed(self) -> List[Pin]:
        """Refreshes the authenticated user's homefeed and returns a list of pins."""
        pins = self._make_request(endpoints.GetHomefeed).json()["resource_response"]["data"]
        
        pins = [Pin(p["grid_title"], p["description"], p["images"],
                    self.base_url + "/pin/" + p["id"],
                    p["rich_summary"]["url"] if p["rich_summary"] else "",
                    p["id"], p["created_at"], p["dominant_color"],
                    p["pinner"]["username"], p["pinner"]["id"],
                    p["board"]["name"], p["board"]["id"], self.base_url + "/" + p["board"]["url"]) for p in pins
                if "ad_destination_url" not in p]
        return pins
    
    def download_pin(self, pin: Pin | int, filepath: str | None = None, overwrite: bool = False) -> str:
        """Downloads a pin, given a Pin object or a pin's id."""
        # not tested with videos
        if type(pin) == Pin:
            url = pin.images["orig"]["url"]
        else:
            # the pin parameter is a pin id
            # not yet implemented
            return
        if not filepath:
            filepath = url.split("/")[-1]
        with open(filepath, "wb+" if overwrite else "wb") as f:
            f.write(self.session.get(url).content)
        return filepath
    
    def search(query: str) -> List[Pin]:
        """Searches Pinterest and returns a list of pins."""
        # not yet implemented
        pass
