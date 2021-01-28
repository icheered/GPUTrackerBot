# GPUTrackerBot
Very crude tracker to track the price of the RTX3080 and send me a message over telegram when it drops below a certain price.

```bash
$ git clone https://github.com/icheered/GPUTrackerBot
$ cd GPUTrackerBot
```

Make a copy of the `config.ini.dist`, call it `config.ini`, and fill out your information.
- API_KEY = Your telegram bot API key. [How to get API key and chat id](https://dev.to/rizkyrajitha/get-notifications-with-telegram-bot-537l).
- CHAT_ID = The chat ID where to send the message to (see link above)
- GPU = Which GPU to track (3080 and 3070 are tested but all others probably work too)
- TARGET = Target price of the GPU. If the price drops below this, a message will be sent. 

### Starting the bot
This program uses poetry for dependency management, but you can use any other dependency manager or virtual environment to install the dependencies:
- beautifulsoup4
- configargparse
- loguru
- requests

If you happen to have poetry installed just execute the following commands:
- `$ poetry shell`
- `$ poetry install`

Then run `$ python main.py` to start the bot
I myself have this running in a TMUX window (terminal multiplexer, basically manager multiple terminal instances in a single terminal) on a server, but this would run fine on a raspberry pi.

If you have TMUX installed:
- `$ tmux new -t gputracker`
- `$ cd GPUtracker`
- `$ poetry shell`
- `$ python main.py`
- `ctrl+b, d` (Press ctrl+b, let go, then press d)

To reattach to the shell
`$tmux a -t gputracker`