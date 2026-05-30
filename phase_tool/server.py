from __future__ import annotations

import base64
import io
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = int(os.environ.get("PHASE_TOOL_PORT", "8765"))


class PhaseToolHandler(BaseHTTPRequestHandler):
    server_version = "PhaseTool/1.0"

    def log_message(self, fmt: str, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args), flush=True)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            self._send_file(ROOT / "index.html")
            return
        requested = (ROOT / path.lstrip("/")).resolve()
        if ROOT not in requested.parents and requested != ROOT:
            self.send_error(403)
            return
        if requested.is_file():
            self._send_file(requested)
            return
        self.send_error(404)

    def do_POST(self):
        if urlparse(self.path).path != "/api/upload":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            image = Image.open(io.BytesIO(raw))
            rgb = image.convert("RGB")
            arr = np.asarray(rgb, dtype=np.uint8)
            gray = np.rint(0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]).astype(np.uint8)

            preview = Image.fromarray(gray, "L")
            png_io = io.BytesIO()
            preview.save(png_io, format="PNG")
            png_b64 = base64.b64encode(png_io.getvalue()).decode("ascii")
            gray_b64 = base64.b64encode(gray.tobytes()).decode("ascii")

            payload = {
                "width": int(gray.shape[1]),
                "height": int(gray.shape[0]),
                "mode": image.mode,
                "format": image.format,
                "previewPng": "data:image/png;base64," + png_b64,
                "grayBase64": gray_b64,
                "name": self.headers.get("X-File-Name", "uploaded-image"),
            }
            self._send_json(payload)
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=400)

    def _send_file(self, path: Path):
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, payload: dict, status: int = 200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    server = ThreadingHTTPServer((HOST, PORT), PhaseToolHandler)
    print(f"Phase tool running at http://{HOST}:{PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
