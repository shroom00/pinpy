# Pinpy

## What is Pinpy?

<img src="./pinpy.png" height=75px>

Pinpy is a wrapper for the Pinterest web API. It aims to mimic requests made when browsing Pinterest on the web. This allows for automation of Pinterest actions via Python.

## Features

<ul>
    <li><a href="#login">Logging in</a> (to perform actions on behalf of a specific user)</li>
    <li><a href="#snd">Searching</a> for pins, videos and boards and downloading them.</li>
</ul>

<h3 id="login">Logging in</h3>

```py
from pinpy import Client


cl = Client("username or email", "password")
```

That's it, now you're logged in!

---
You can also save the session to a file so you don't have to login again later.

```py
cl = Client("username or email", "password")
cl.save_session("session_file")
```

This will save the session to a file called *session_file*.

---
To reuse the session later on, pass the `session` argument when initialising `Client`. `session` should be the filepath of the previously saved session. Username/email and password are ignored when loading from a file.

```py
cl = Client(session="session_file")
```

---

<h3 id="snd">Searching and Downloading</h3>

**NOTE:** Searching doesn't require a login.

```py
from pinpy import Client


cl = Client()
pins = cl.search("football")
```

This will search Pinterest for *football*. A `Results` object is returned.
`Results` are like a page of search results. You can iterate over them, and also use the `next_page` method to get the next page of results.
When iterating over the results, `Pin` objects are returned. `Pin` objects represent pins, as the name implies. You can use the `download` method of a `Pin` to download it. If there are no pages remaining, `next_page` will return `None`.

---

```py
pins = cl.search("football")

for pin in pins:
    download_pin(pin)

```

Downloading a pin will return the filepath of the image/video downlaoded. The filepath is optional; a name will be chosen automatically if one isn't given. (The naming format is "pin_(pin_id).filetype")
