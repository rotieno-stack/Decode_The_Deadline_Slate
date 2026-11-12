"""
LOCAL TEST SERVER -- for trying the puzzle without Slate. Not part of the
Slate deployment (it keeps the solution in this file, for testing only).

Run:   python server.py        (from inside the local-test folder)
Open:  http://localhost:8000/

It mimics the two Slate query web services:
  /guess?row=0&col=0&value=7  ->  {"result":{"correct":"true"}}
  /hint?row=0&col=0           ->  {"result":{"odd":"true","prime":"true"}}
and serves ../puzzle.html with the endpoint URLs filled in automatically.
"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

PORT = 8000
SOLUTION = [[7, 3, 5], [2, 9, 4], [6, 8, 1]]
PRIMES = {2, 3, 5, 7}
PAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "puzzle.html")


def to_int(q, name):
    try:
        return int(q.get(name, [None])[0])
    except (TypeError, ValueError):
        return None


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, payload):
        self._send(200, json.dumps(payload), "application/json")

    def do_GET(self):
        url = urlparse(self.path)
        q = parse_qs(url.query)

        if url.path in ("/", "/index.html", "/puzzle.html"):
            with open(PAGE, encoding="utf-8") as f:
                html = f.read()
            base = f"http://localhost:{PORT}"
            html = html.replace("PASTE_GUESS_ENDPOINT_HERE", f"{base}/guess")
            html = html.replace("PASTE_HINT_ENDPOINT_HERE", f"{base}/hint")
            page = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                    '<meta name="viewport" content="width=device-width, initial-scale=1">'
                    '<title>Decode the Deadline (local test)</title></head>'
                    '<body style="margin:0;background:#0e1116">' + html + "</body></html>")
            return self._send(200, page, "text/html; charset=utf-8")

        r, c = to_int(q, "row"), to_int(q, "col")
        if url.path in ("/guess", "/hint"):
            if r is None or c is None or not (0 <= r < 3 and 0 <= c < 3):
                return self._json({})  # like Slate: empty result for bad input
            val = SOLUTION[r][c]
            if url.path == "/guess":
                v = to_int(q, "value")
                return self._json({"result": {"correct": "true" if v == val else "false"}})
            return self._json({"result": {"odd": "true" if val % 2 else "false",
                                          "prime": "true" if val in PRIMES else "false"}})

        self._send(404, "Not found", "text/plain")

    def log_message(self, fmt, *args):
        pass  # keep the terminal quiet


if __name__ == "__main__":
    print(f"Decode the Deadline test server running: http://localhost:{PORT}/")
    print("Press Ctrl+C to stop.")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
