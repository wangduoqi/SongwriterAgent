"""Tool schemas (sent to Claude) and dispatcher (executes the calls)."""
import json
import storage
import suno_client


# Tool schemas advertised to Claude via the API.
TOOLS = [
    {
        "name": "submit_suno_generation",
        "description": (
            "Submit lyrics and a style prompt to Suno for music generation. "
            "Creates a new version of the current song. Call this only when the "
            "user has approved the lyrics and is ready to hear audio."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "lyrics": {
                    "type": "string",
                    "description": "Full lyrics with [Verse]/[Chorus]/[Bridge] markers.",
                },
                "style_prompt": {
                    "type": "string",
                    "description": "Suno style string, e.g. 'city pop, mellow female vocal, warm synths, 90s'.",
                },
                "notes": {
                    "type": "string",
                    "description": "Optional: what changed vs the previous version.",
                },
            },
            "required": ["lyrics", "style_prompt"],
        },
    },
    {
        "name": "check_suno_status",
        "description": "Check status of a submitted Suno job by job_id.",
        "input_schema": {
            "type": "object",
            "properties": {"job_id": {"type": "string"}},
            "required": ["job_id"],
        },
    },
    {
        "name": "download_audio",
        "description": "Download the finished audio for a completed job and attach it to the given version.",
        "input_schema": {
            "type": "object",
            "properties": {
                "job_id": {"type": "string"},
                "version_num": {"type": "integer"},
            },
            "required": ["job_id", "version_num"],
        },
    },
    {
        "name": "list_versions",
        "description": "List all versions of the current song with summaries.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_version",
        "description": "Fetch full details of one version (including full lyrics).",
        "input_schema": {
            "type": "object",
            "properties": {"version_num": {"type": "integer"}},
            "required": ["version_num"],
        },
    },
    {
        "name": "mark_final",
        "description": "Lock in a version as the final chosen one for this song.",
        "input_schema": {
            "type": "object",
            "properties": {"version_num": {"type": "integer"}},
            "required": ["version_num"],
        },
    },
]


def dispatch(tool_name: str, tool_input: dict, song_id: int) -> str:
    """Execute a tool and return a JSON string result for Claude to consume."""
    try:
        if tool_name == "submit_suno_generation":
            lyrics = tool_input["lyrics"]
            style = tool_input["style_prompt"]
            notes = tool_input.get("notes", "")
            resp = suno_client.submit_generation(lyrics, style)
            _vid, version_num = storage.add_version(
                song_id, lyrics, style,
                suno_job_id=resp["job_id"],
                metadata={"notes": notes},
            )
            return json.dumps({
                "job_id": resp["job_id"],
                "version_num": version_num,
                "status": resp["status"],
                "hint": "Poll check_suno_status until status='complete', then download_audio.",
            })

        if tool_name == "check_suno_status":
            return json.dumps(suno_client.check_status(tool_input["job_id"]))

        if tool_name == "download_audio":
            job_id = tool_input["job_id"]
            version_num = tool_input["version_num"]
            version = storage.get_version(song_id, version_num)
            if not version:
                return json.dumps({"error": f"version {version_num} not found"})
            song = storage.get_song(song_id)
            safe_title = song["title"].replace(" ", "_").replace("/", "_")
            dest_name = f"{safe_title}_v{version_num}"
            result = suno_client.download_audio(job_id, dest_name)
            if "path" in result:
                storage.update_version(
                    version["id"],
                    audio_path=result["path"],
                    status="complete",
                )
            return json.dumps(result)

        if tool_name == "list_versions":
            versions = storage.list_versions(song_id)
            return json.dumps([
                {
                    "version_num": v["version_num"],
                    "status": v["status"],
                    "is_final": bool(v["is_final"]),
                    "has_audio": bool(v["audio_path"]),
                    "style_prompt": v["style_prompt"],
                    "lyrics_preview": (v["lyrics"] or "")[:180],
                    "created_at": v["created_at"],
                }
                for v in versions
            ])

        if tool_name == "get_version":
            v = storage.get_version(song_id, tool_input["version_num"])
            if not v:
                return json.dumps({"error": "not found"})
            return json.dumps(v)

        if tool_name == "mark_final":
            ok = storage.mark_final(song_id, tool_input["version_num"])
            return json.dumps({"ok": ok, "final_version": tool_input["version_num"]})

        return json.dumps({"error": f"unknown tool: {tool_name}"})

    except Exception as e:
        return json.dumps({"error": str(e), "tool": tool_name})