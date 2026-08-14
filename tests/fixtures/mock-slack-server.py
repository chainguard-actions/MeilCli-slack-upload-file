#!/usr/bin/env python3
"""
Mock Slack API server for testing slack-upload-file action.
Handles the filesUploadV2 flow:
1. POST /api/files.getUploadURLExternal -> returns upload_url and file_id
2. POST /upload -> accepts file upload (multipart/form-data)
3. POST /api/files.completeUploadExternal -> returns file info
4. POST /api/files.delete -> handles file deletion
"""
import http.server
import json
import sys
from http.server import ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000

class SlackMockHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write("[mock-slack] %s\n" % (format % args))
        sys.stderr.flush()

    def send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def drain_body(self):
        """Read and discard the request body."""
        try:
            transfer_encoding = self.headers.get('Transfer-Encoding', '')
            content_length = self.headers.get('Content-Length', '0')
            if 'chunked' in transfer_encoding.lower():
                # Read chunked body
                while True:
                    line = self.rfile.readline().strip()
                    chunk_size = int(line, 16)
                    if chunk_size == 0:
                        self.rfile.readline()  # trailing CRLF
                        break
                    self.rfile.read(chunk_size)
                    self.rfile.readline()  # CRLF after chunk
            else:
                length = int(content_length)
                if length > 0:
                    self.rfile.read(length)
        except Exception:
            pass

    def do_POST(self):
        self.drain_body()
        path = self.path.split('?')[0]

        if 'files.getUploadURLExternal' in path:
            self.send_json({
                "ok": True,
                "upload_url": "http://localhost:%d/upload" % PORT,
                "file_id": "F12345TEST"
            })
        elif path == '/upload' or path.startswith('/upload?') or path.startswith('/upload/'):
            self.send_json({"ok": True})
        elif 'files.completeUploadExternal' in path:
            # filesUploadV2 wraps each completeUploadExternal response in the outer 'files' array.
            # The code accesses result.files[i].files[j].id, so each completeUploadExternal
            # response must have a 'files' array of file objects.
            self.send_json({
                "ok": True,
                "files": [
                    {
                        "id": "F12345TEST",
                        "name": "test-file.txt",
                        "title": "Test File",
                        "permalink": "https://example.slack.com/files/U123/F12345TEST/test-file.txt"
                    }
                ]
            })
        elif 'files.delete' in path:
            self.send_json({"ok": True})
        else:
            # Generic OK for any other Slack API call
            self.send_json({"ok": True})

    def do_PUT(self):
        self.drain_body()
        # Handle file upload via PUT (some Slack SDK versions use PUT for upload_url)
        self.send_json({"ok": True})

    def do_GET(self):
        self.drain_body()
        self.send_json({"ok": True, "status": "mock-slack-server-running"})

if __name__ == '__main__':
    server = ThreadingHTTPServer(('0.0.0.0', PORT), SlackMockHandler)
    sys.stderr.write("[mock-slack] Starting mock Slack API server on port %d\n" % PORT)
    sys.stderr.flush()
    server.serve_forever()
