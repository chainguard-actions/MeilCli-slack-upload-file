#!/usr/bin/env python3
"""Minimal mock of the Slack Web API endpoints used by filesUploadV2.

Usage: mock_slack.py PORT LOGFILE [mode]
mode: "ok" (default) or "invalid_auth"
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(sys.argv[1])
LOG = sys.argv[2]
MODE = sys.argv[3] if len(sys.argv) > 3 else "ok"
counter = {"n": 0}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, ctype="application/json"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(200, json.dumps({"ok": True}))

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        with open(LOG, "ab") as f:
            f.write(("POST %s\n" % self.path).encode())
            f.write(body + b"\n")
        path = self.path.split("?")[0]
        if MODE == "invalid_auth" and path.startswith("/api/"):
            self._send(200, json.dumps({"ok": False, "error": "invalid_auth"}))
            return
        if path.endswith("files.getUploadURLExternal"):
            counter["n"] += 1
            fid = "FMOCK%d" % counter["n"]
            self._send(200, json.dumps({
                "ok": True,
                "upload_url": "http://127.0.0.1:%d/upload/%s" % (PORT, fid),
                "file_id": fid,
            }))
        elif path.startswith("/upload/"):
            self._send(200, "OK", "text/plain")
        elif path.endswith("files.completeUploadExternal"):
            files = []
            try:
                from urllib.parse import parse_qs
                qs = parse_qs(body.decode())
                files = json.loads(qs.get("files", ["[]"])[0])
            except Exception:
                files = []
            if not files:
                files = [{"id": "FMOCK1"}]
            self._send(200, json.dumps({
                "ok": True,
                "files": [{"id": f.get("id"), "title": f.get("title", "")} for f in files],
            }))
        else:
            self._send(200, json.dumps({"ok": True}))

    def log_message(self, fmt, *args):
        pass


HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
