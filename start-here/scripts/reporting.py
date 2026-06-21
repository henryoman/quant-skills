"""Small static HTML report helper for standalone skill scripts."""

from __future__ import annotations

import datetime as dt
import html
from pathlib import Path
from typing import Iterable


def _esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def _status_label(status: str) -> str:
    normalized = status.lower()
    if normalized == "pass":
        return "Right"
    if normalized == "warn":
        return "Needs Review"
    if normalized == "fail":
        return "Wrong"
    return "Info"


def _rows(items: Iterable[dict[str, object]]) -> str:
    body = []
    for item in items:
        status = str(item.get("status", "info")).lower()
        body.append(
            "<tr>"
            f"<td><span class=\"pill {status}\">{_esc(_status_label(status))}</span></td>"
            f"<td>{_esc(item.get('name', ''))}</td>"
            f"<td>{_esc(item.get('detail', ''))}</td>"
            "</tr>"
        )
    return "\n".join(body)


def _output_rows(items: Iterable[dict[str, object]]) -> str:
    body = []
    for item in items:
        body.append(
            "<tr>"
            f"<td>{_esc(item.get('name', ''))}</td>"
            f"<td><code>{_esc(item.get('path', ''))}</code></td>"
            f"<td>{_esc(item.get('detail', ''))}</td>"
            "</tr>"
        )
    return "\n".join(body)


def write_html_report(
    path: Path,
    *,
    title: str,
    summary: str,
    checks: list[dict[str, object]],
    outputs: list[dict[str, object]],
    notes: list[str] | None = None,
) -> None:
    """Write a self-contained report showing what passed, needs review, or failed."""

    now = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    status_counts = {status: sum(1 for item in checks if item.get("status") == status) for status in ["pass", "warn", "fail"]}
    notes = notes or []
    note_items = "\n".join(f"<li>{_esc(note)}</li>" for note in notes) or "<li>No follow-up notes.</li>"
    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{_esc(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fb;
      --ink: #18202a;
      --muted: #596574;
      --line: #d9dee7;
      --panel: #ffffff;
      --pass: #177245;
      --warn: #9a6100;
      --fail: #b42318;
      --info: #315da8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }}
    main {{ width: min(1080px, calc(100% - 32px)); margin: 32px auto 56px; }}
    header, section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 16px;
    }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }}
    h2 {{ margin: 0 0 14px; font-size: 18px; letter-spacing: 0; }}
    p {{ margin: 0; color: var(--muted); }}
    .stats {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
    .stat {{ border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; min-width: 120px; }}
    .stat b {{ display: block; font-size: 22px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th, td {{ text-align: left; border-top: 1px solid var(--line); padding: 10px 8px; vertical-align: top; }}
    th {{ color: var(--muted); font-weight: 650; }}
    code {{ overflow-wrap: anywhere; }}
    ul {{ margin: 0; padding-left: 20px; color: var(--muted); }}
    .pill {{ display: inline-block; border-radius: 999px; padding: 3px 9px; font-size: 12px; font-weight: 700; }}
    .pass {{ color: var(--pass); background: #e8f5ee; }}
    .warn {{ color: var(--warn); background: #fff4df; }}
    .fail {{ color: var(--fail); background: #fdebea; }}
    .info {{ color: var(--info); background: #edf3ff; }}
    @media (max-width: 680px) {{
      main {{ width: min(100% - 20px, 1080px); margin-top: 12px; }}
      header, section {{ padding: 14px; }}
      table, thead, tbody, tr, th, td {{ display: block; }}
      th {{ display: none; }}
      td {{ border-top: 0; padding: 6px 0; }}
      tr {{ border-top: 1px solid var(--line); padding: 8px 0; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{_esc(title)}</h1>
      <p>{_esc(summary)}</p>
      <p>Generated {now}</p>
      <div class="stats">
        <div class="stat"><b>{status_counts['pass']}</b>Right</div>
        <div class="stat"><b>{status_counts['warn']}</b>Needs Review</div>
        <div class="stat"><b>{status_counts['fail']}</b>Wrong</div>
      </div>
    </header>
    <section>
      <h2>Checks</h2>
      <table>
        <thead><tr><th>Status</th><th>Check</th><th>Detail</th></tr></thead>
        <tbody>{_rows(checks)}</tbody>
      </table>
    </section>
    <section>
      <h2>Outputs</h2>
      <table>
        <thead><tr><th>Name</th><th>Path</th><th>Detail</th></tr></thead>
        <tbody>{_output_rows(outputs)}</tbody>
      </table>
    </section>
    <section>
      <h2>Next Actions</h2>
      <ul>{note_items}</ul>
    </section>
  </main>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")
