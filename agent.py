"""Core agent loop: user message -> Claude -> tool calls -> ... -> final text."""
import anthropic
import config
import storage
import tools as tools_module

_client = anthropic.Anthropic()

# Safety cap so a misbehaving loop can't burn through your API quota.
MAX_TOOL_ITERATIONS = 10


def run_turn(song_id: int, user_message: str, verbose: bool = True) -> str:
    """Run one user turn end-to-end. Persists all messages to the song's history."""
    history = storage.load_messages(song_id)
    history.append({"role": "user", "content": user_message})
    storage.save_message(song_id, "user", user_message)

    final_text_parts: list[str] = []

    for _ in range(MAX_TOOL_ITERATIONS):
        response = _client.messages.create(
            model=config.ANTHROPIC_MODEL,
            max_tokens=config.MAX_TOKENS,
            # cache_control on the system prompt saves input tokens on every
            # iteration after the first - meaningful for a creative REPL.
            system=[{
                "type": "text",
                "text": config.SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            tools=tools_module.TOOLS,
            messages=history,
        )

        # Persist assistant content blocks (dict form so we can round-trip them)
        assistant_blocks = [b.model_dump() for b in response.content]
        history.append({"role": "assistant", "content": assistant_blocks})
        storage.save_message(song_id, "assistant", assistant_blocks)

        # Stream any text to the console
        for block in response.content:
            if block.type == "text":
                final_text_parts.append(block.text)
                if verbose:
                    print(block.text)

        if response.stop_reason != "tool_use":
            break

        # Execute every tool_use block, collect results
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if verbose:
                    keys = list(block.input.keys())
                    print(f"\n  → {block.name}({', '.join(keys)})")
                result = tools_module.dispatch(block.name, block.input, song_id)
                if verbose:
                    preview = result if len(result) <= 180 else result[:180] + "..."
                    print(f"  ← {preview}\n")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        # Feed tool results back as the next user turn
        history.append({"role": "user", "content": tool_results})
        storage.save_message(song_id, "user", tool_results)

    return "".join(final_text_parts)