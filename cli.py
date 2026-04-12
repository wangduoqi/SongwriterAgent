"""Interactive CLI for the songwriter agent.

Commands:
  /new <title>     create a new song
  /list            list all songs
  /switch <id>     switch to a song
  /versions        list versions of current song
  /help            show help
  /quit            exit

Anything else is sent to the agent for the currently active song.
"""
import storage
import agent

BANNER = r"""
  _____                            _ _
 / ____|                          (_) |
| (___   ___  _ __   __ _ _      ___| |_ ___ _ __
 \___ \ / _ \| '_ \ / _` \ \ /\ / / | __/ _ \ '__|
 ____) | (_) | | | | (_| |\ V  V /| | ||  __/ |
|_____/ \___/|_| |_|\__, | \_/\_/ |_|\__\___|_|
                     __/ |
                    |___/
  agent REPL - type /help for commands
"""

HELP = """Commands:
  /new <title>     create a new song
  /list            list all songs
  /switch <id>     switch to a song by id
  /versions        list versions of the current song
  /help            show this help
  /quit            exit
Anything else is sent to the agent."""


def cmd_list():
    songs = storage.list_songs()
    if not songs:
        print("(no songs yet - use /new <title>)")
        return
    for s in songs:
        print(f"  #{s['id']:>3}  {s['title']}  ({s['created_at']})")


def cmd_versions(song_id):
    if not song_id:
        print("(no song selected)")
        return
    versions = storage.list_versions(song_id)
    if not versions:
        print("(no versions yet)")
        return
    for v in versions:
        flags = []
        if v["is_final"]:
            flags.append("FINAL")
        if v["audio_path"]:
            flags.append("audio")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        style = (v["style_prompt"] or "")[:55]
        print(f"  v{v['version_num']:>2}  {v['status']:<12}{flag_str}  {style}")


def main():
    storage.init_db()
    print(BANNER)

    current = None
    songs = storage.list_songs()
    if songs:
        current = songs[0]["id"]
        print(f"[resumed song #{current}: '{songs[0]['title']}']")
    else:
        print("[no songs yet - run /new <title> to start]")

    while True:
        try:
            prompt = f"\nsong#{current}> " if current else "\n(no song)> "
            line = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue

        if line.startswith("/"):
            parts = line[1:].split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd in ("quit", "exit"):
                break
            elif cmd == "help":
                print(HELP)
            elif cmd == "new":
                if not arg:
                    print("usage: /new <title>")
                else:
                    current = storage.create_song(arg)
                    print(f"created song #{current}: {arg}")
            elif cmd == "list":
                cmd_list()
            elif cmd == "switch":
                try:
                    sid = int(arg)
                except ValueError:
                    print("usage: /switch <id>")
                    continue
                if storage.get_song(sid):
                    current = sid
                    print(f"switched to #{sid}")
                else:
                    print("not found")
            elif cmd == "versions":
                cmd_versions(current)
            else:
                print(f"unknown command: /{cmd}  (try /help)")
            continue

        # Otherwise: send to the agent
        if not current:
            print("create a song first: /new <title>")
            continue
        print()
        try:
            agent.run_turn(current, line)
        except Exception as e:
            print(f"\n[agent error] {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()