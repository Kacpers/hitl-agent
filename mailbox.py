"""Test mailbox as an MCP server: the same tool names as a real mail server, but it only writes files to disk."""
import datetime
import json
import pathlib

from mcp.server.mcpserver import MCPServer

ROOT = pathlib.Path(__file__).resolve().parent
mcp = MCPServer("mailbox", instructions="Shop test mailbox (fictional data).")


def unmask(text):
    """Placeholders from pseudonymize.py back to data: this server's code does it, the model never sees the map."""
    path = ROOT / "placeholders.json"
    mapping = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text


def save(folder, to, subject, body):
    to, subject, body = unmask(to), unmask(subject), unmask(body)
    (ROOT / folder).mkdir(exist_ok=True)
    path = ROOT / folder / f"{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
    path.write_text(f"To: {to}\nSubject: {subject}\n\n{body}\n", encoding="utf-8")
    return str(path.relative_to(ROOT))


@mcp.tool()
def create_draft(to: str, subject: str, body: str) -> str:
    """Saves a draft mail. Sends nothing."""
    return f"draft saved: {save('drafts', to, subject, body)}"


@mcp.tool()
def send_message(to: str, subject: str, body: str) -> str:
    """SENDS a mail to the recipient. Cannot be undone."""
    return f"sent: {save('sent', to, subject, body)}"


if __name__ == "__main__":
    mcp.run()
