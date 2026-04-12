# Songwriter Agent — Minimal Skeleton

CLI-driven agent that uses Claude + Suno (stubbed for now) to iteratively write songs.

## Setup

```bash
cd songwriter_agent
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python cli.py
```

## Usage

```
/new 湾区通勤           # create a new song
write a city pop song about the morning commute on 880 N, mellow, female vocal
# ... claude drafts lyrics in chat ...
副歌再抓耳一点，加一个 hook
# ... iterate ...
ok 满意了，提交 Suno 生成                    # agent calls submit_suno_generation
查一下 job 状态                                # agent calls check_suno_status
下载 v1                                        # agent calls download_audio
/versions                                      # list all versions of this song
```

## Architecture

```
cli.py          REPL, dispatches slash-commands, forwards chat to agent
 └─ agent.py    run_turn() - the Claude tool-use loop, persists history
     ├─ tools.py        tool schemas (sent to Claude) + dispatch()
     │   └─ suno_client.py   Suno API (currently STUB - replace for real use)
     └─ storage.py      SQLite: songs, versions, messages
 config.py      model name, paths, system prompt
```

Each song gets its own conversation history (stored in SQLite), so switching
between songs preserves context per song.

## Replacing the Suno stub

Edit `suno_client.py` — three functions to implement against the real API:

- `submit_generation(lyrics, style_prompt)` → `{'job_id', 'status'}`
- `check_status(job_id)` → `{'job_id', 'status', ...}`
- `download_audio(job_id, dest_name)` → `{'job_id', 'path', 'size_bytes'}`

Tool schemas and storage layer stay the same.

## Extending

**Add a tool:** add an entry to `TOOLS` in `tools.py`, then add a branch in `dispatch()`.

**Add a project (e.g. trading ops):** duplicate `config.py`'s `SYSTEM_PROMPT` +
`TOOLS` as a separate project config, then have `agent.run_turn` take a project
param that selects which bundle to load. Store each project's conversations
in a separate table or scope messages by a `project` column.

**Prompt caching:** already enabled on the system prompt. To also cache the
tools block (larger savings), add `cache_control` to the last tool in the list.

## Safety notes (relevant to your broader agent plans)

- All Claude can do is call the 6 tools in `tools.py`. It can't execute
  arbitrary code, touch the filesystem outside `data/audio`, or make network
  calls beyond Anthropic + Suno.
- No human-confirmation gate is wired in yet — unnecessary for creative work.
  When you build the trading-ops project on this same framework, add a
  `requires_confirmation` flag to risky tools and pause in `dispatch()` until
  the user approves.
- `MAX_TOOL_ITERATIONS = 10` in `agent.py` caps runaway loops.