# Hockey Team Bot

A Discord bot for running a hockey team. It keeps the roster, match schedule, attendance and results in one place, and adds score predictions and some fun on top.

## Features

- Team roster and lineup (`!sestava`) with player positions
- Match schedule: add matches and list upcoming games
- Attendance tracking (`!prijdu`, `!neprijdu`, `!dochazka`)
- Match results history and personal stats
- Score predictions (tips) with a leaderboard
- Hockey quiz, face-off game, tactics tips and motivation messages
- Team ping and role info
- Data stored in simple JSON files, no database needed

## Tech Stack

- Python 3.10+
- discord.py

## Getting Started

### Prerequisites

- Python 3.10+
- A Discord bot token with **Message Content** and **Server Members** intents enabled

### Installation

```bash
git clone https://github.com/Exo-Studios-Code/hockey-team-bot.git
cd hockey-team-bot
pip install -r requirements.txt
```

### Configuration

Set your bot token as an environment variable.

Linux/macOS:

```bash
export DISCORD_TOKEN=your_bot_token
```

Windows PowerShell:

```powershell
$env:DISCORD_TOKEN="your_bot_token"
```

Edit the default `TEAM_MEMBERS` dictionary in `bot.py` to match your roster.

### Run

```bash
python bot.py
```

The `data/` folder is created automatically on first start.

## Commands

Prefix: `!`

| Command | Description |
|---------|-------------|
| `!sestava` | Show the lineup |
| `!training` | Training info |
| `!pridatzapas <type> <date> <time>` | Add a match |
| `!zapasy` | List scheduled matches |
| `!prijdu` / `!neprijdu` | Confirm or decline attendance |
| `!dochazka` | Show attendance |
| `!mojestats` | Your personal stats |
| `!zapiszapas <date> <result>` | Save a match result |
| `!vysledky` | Results history |
| `!tip <result>` | Predict the next result |
| `!vsechnytipy` / `!tiprank` | All tips and tip leaderboard |
| `!faceoff` `!hokejquiz` `!motivace` `!taktika <type>` | Fun and tactics |
| `!pingteam` `!myrole` | Team ping and role info |
