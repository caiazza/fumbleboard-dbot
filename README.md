# fumbleboard-dbot
A Discord bot to access the fumble board


## Requirements
This bot requires the discord API with voice support enabled, which can be installed with the following command
```bash
python3 -m pip install -U discord.py[voice]
```

On Linux environments, installing voice requires getting the following dependencies:
* libffi
* libnacl
* python3-dev

For a Debian-based system, the following command will get these dependencies:

```bash
$ apt install libffi-dev libnacl-dev python3-dev
```

Additionally it requires the `dotenv` that can be installed with 
```bash
python3 -m pip install -U python-dotenv
```