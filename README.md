# slack-mathoid
Math rendering as a Slack integration via Wikimedia Mathoid.

## Try it out!
Simply add `https://puck.dmoj.ca/typeset` as an outgoing webhook in your Slack channel.

You can trigger slack-mathoid by prefixing LaTeX commands with `!math`.

![slack-mathoid in action](http://i.imgur.com/7xeeVYZ.png)

## Installation
slack-mathoid setup is easy.

```shell
$ git clone https://github.com/Xyene/slack-mathoid.git
$ cd slack-mathoid
$ python setup.py develop
```

## Running slack-mathoid
To start slack-mathoid, simply run:
```shell
export MATHOID_URL="http://localhost:10044"
export MATHOID_CACHE="/web/static"
export MATHOID_SERVE_URL="https://math.example.org"
slack-mathoid --port=8888
```

This will start a Slack webhook on `localhost:8888/typset`, which should be forwarded and added as an outgoing webhook on Slack.
Cached math will be stored in `MATHOID_CACHE`, and served off `MATHOID_SERVE_URL`. slack-mathoid assumes a Mathoid server is running
on `MATHOID_URL`.

You may optionally provide a `SLACK_AUTH_TOKEN` environment variable to restrict access to the server.
