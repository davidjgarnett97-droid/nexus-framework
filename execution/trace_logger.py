"""
Nexus Trace Logger — execution/nexus/trace_logger.py

Records per-tool-call execution traces to .data/traces/traces.jsonl.
Separate from the audit log (audit log = decisions; trace log = tool executions).

Called from Claude Code hooks:
  PreToolUse:  python trace_logger.py pre  (stdin = hook context JSON)
  PostToolUse: python trace_logger.py post (stdin = hook context JSON)

Always exits 0 — never blocks Claude Code execution.
"""
import hashlib
import json
import os
import sys
import time

TRACE_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "execution", ".data", "traces.jsonl"
)
# Normalize to absolute path
TRACE_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".data", "traces.jsonl")
)

# Tools that are too noisy to trace individually — aggregate only
_SKIP_TRACE = {"Read", "Glob"}

# Max bytes for input/output snapshots in the trace
_SNAP_LIMIT = 512


def _hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8", errors="replace")).hexdigest()[:12]


def _snap(value) -> str:
    """Truncated string snapshot of a value for the trace record."""
    try:
        s = json.dumps(value, ensure_ascii=False)
    except Exception:
        s = str(value)
    return s[:_SNAP_LIMIT] + ("…" if len(s) > _SNAP_LIMIT else "")


def _write(record: dict) -> None:
    os.makedirs(os.path.dirname(TRACE_FILE), exist_ok=True)
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] not in ("pre", "post"):
        sys.exit(0)

    mode = sys.argv[1]

    try:
        raw = sys.stdin.read()
        ctx = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    tool_name = ctx.get("tool_name") or ctx.get("tool", "")

    if tool_name in _SKIP_TRACE:
        sys.exit(0)

    try:
        tool_input = ctx.get("tool_input") or ctx.get("input") or {}
        ts = time.time()

        if mode == "pre":
            record = {
                "ts": ts,
                "event": "pre_tool",
                "tool": tool_name,
                "input_hash": _hash(json.dumps(tool_input, sort_keys=True)),
                "input_snap": _snap(tool_input),
                "session_id": ctx.get("session_id", ""),
            }
        else:
            tool_response = ctx.get("tool_response") or ctx.get("output") or {}
            record = {
                "ts": ts,
                "event": "post_tool",
                "tool": tool_name,
                "input_hash": _hash(json.dumps(tool_input, sort_keys=True)),
                "output_hash": _hash(json.dumps(tool_response, sort_keys=True)),
                "output_snap": _snap(tool_response),
                "session_id": ctx.get("session_id", ""),
            }

        _write(record)
    except Exception:
        pass  # never block Claude Code

    sys.exit(0)


if __name__ == "__main__":
    main()
