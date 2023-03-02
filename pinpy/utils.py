import json
import re
from . import endpoints
from .exceptions import PinterestError
from .objects import Pin
import requests
import dill
from os import path


def make_pin_from_json(json_: dict, video_url: str = None) -> Pin:
    """Creates a Pin object from a json dict received from Pinterest."""
    return Pin(
        json_["grid_title"],
        json_["description"].strip(),
        json_["images"],
        video_url,
        f"https://www.pinterest.com/pin/{json_['id']}",
        json_["id"],
        json_["created_at"],
        json_["dominant_color"],
        json_["pinner"]["username"],
        json_["pinner"]["id"],
        json_["board"]["name"],
        json_["board"]["id"] if "id" in json_["board"] else None,
        f"https://www.pinterest.com{json_['board']['url']}",
        "image" if json_["videos"] is None else "video",
    )


def make_board_from_json(session: requests.sessions.Session, json: dict):
    return


def get_resource(resource: dict):
    if resource["type"] == "pin":
        resource = make_pin_from_json(resource)
    elif resource["type"] == "board":
        resource = make_board_from_json(resource)
    else:
        raise NotImplemented(f"Type: {resource['type']} needs to be implemented")
    return resource


def get_resources(
    pins: dict,
    ignore_ads: bool = True,
):
    """Gets pins and boards from a results page's json.
    Used for home feed and search results.
    Ignores ads by default"""
    data = pins["resource_response"]["data"]
    if "results" in data:  # is "results" always present? further enquiry needed.
        data = data["results"]
    # results with type "story" need handling
    resources = []
    if ignore_ads:
        for resource in data:
            if ("ad_destination_url" not in resource) and (resource["type"] != "story"):
                resources.append(get_resource(resource))
    else:
        for resource in data:
            if resource["type"] != "story":
                resources.append(get_resource(resource))
    return resources


def make_request(
    session, endpoint: endpoints.Endpoint, *args, **kwargs
) -> requests.Response:
    """Utility function to make a request to an endpoint and handle errors."""
    e: endpoints.Endpoint = endpoint(*args, **kwargs)
    url = e.url

    headers: dict = session.headers
    if e.fresh_headers:
        headers = e.headers
    else:
        headers.update(e.headers)

    if e.method == "get":
        response = session.get(url)
    elif e.method == "post":
        if e.data:
            response = session.post(url, data=e.data, headers=headers)
        else:
            response = session.post(url, json=e.json, headers=headers)

    session.cookies.update(response.cookies)
    session.headers["Cookie"] = "; ".join(
        [f"{cookie.name}={cookie.value}" for cookie in session.cookies]
    )

    if "application/json" in response.headers.get("Content-Type", ""):
        if "error" in response.json() or (
            "status" in response.json()
            and response.json()["status"] in ["failure", 400]
        ):
            raise PinterestError(response)
    return response


def load_session(filename) -> None:
    """Loads a session from a previous instance to avoid logging in multiple times."""
    with open(filename, "rb") as f:
        session = dill.load(f)
    return session


def get_pin(
    pin_id: int | str, session: requests.sessions.Session = requests.sessions.session()
) -> Pin:
    """Returns a Pin object, given a pin's id or url"""
    if type(pin_id) == str:
        if not pin_id.isnumeric():
            pin_id = pin_id.removesuffix("/").split("/")[-1]
    pin = make_request(session, endpoints.GetPin, pin_id).text
    video_url = re.findall(r"video-snippet.+?contentUrl\":\"(.+?)\"", pin, re.DOTALL)[0]
    pin = json.loads(re.findall(r"__PWS_DATA__.+?>(.+?)</script>", pin, re.DOTALL)[0])[
        "props"
    ]["initialReduxState"]["resources"]["PinResource"]
    pin = pin[list(pin.keys())[0]]["data"]
    return make_pin_from_json(session, pin, video_url)


def download_pin(
    pin: Pin | int | str,
    filename: str,
    dir_filepath: str,
    session: requests.sessions.Session,
) -> str:
    """Downloads a pin, given a Pin object, a pin's id or a pin's url."""
    if type(pin) != Pin:
        pin = get_pin(pin, session)
    if pin.media_type == "image":
        url = pin.images["orig"]["url"]
    else:
        if not pin.video_url:
            pin.video_url = get_pin(pin.pin_id, session).video_url
        url = pin.video_url
    if not filename:
        filename = f"pin_{pin.pin_id}.{url.split('.')[-1]}"
    fp = path.join(dir_filepath, filename)
    with open(fp, "wb") as f:
        f.write(session.get(url).content)
    return fp
