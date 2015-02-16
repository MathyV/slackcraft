# slackcraft

This is a Slack bot for World of Warcraft players that is built on the excellent Slask project. You need to have Slask installed to use these plugins.

# How to use this

* Create a virtualenv
* Clone Slask from my repo (until all changes are merged upstream)
* Clone battlenet from my repo (until all changes are merged upstream)
* Clone this repo
* Install dependencies
* Get the necessary keys
* Create a config.py
* Start the bot and invite it to the channels you want it in
* Have fun

https://github.com/MathyV/battlenet

```
$ virtualenv -p python2.7 env
$ source env/bin/activate
$ git clone https://github.com/MathyV/slask
$ git clone https://github.com/MathyV/battlenet
$ git clone https://github.com/MathyV/slackcraft
$ pip install sqlalchemy humanize
$ pip install -r slask/requirements.txt
$ pip install -r battlenet/requirements.txt
$ cd battlenet/
$ python setup.py install
$ cd ../slackcraft/
$ cp config.py.sample config.py
$ nano config.py
$ python ../slask/slask.py -p ./
```

# Currently implemented

* !help
* !status

# Todo

* Make more plugins
* Make better documentation
* Clean up

Really, this is just a very early mock-up of some code, it needs improving