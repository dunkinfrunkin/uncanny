"""Local web server for the uncanny visualizer."""

from __future__ import annotations

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from uncanny.analyzers.compression import CompressionAnalyzer
from uncanny.analyzers.burstiness import BurstinessAnalyzer
from uncanny import ensemble

STATIC_DIR = Path(__file__).parent / "static"


def _analyze(text: str, fast: bool = False) -> dict:
    """Run analysis and return results as dict."""
    analyzers = [CompressionAnalyzer()]
    if not fast:
        analyzers.append(BurstinessAnalyzer())

    try:
        from uncanny.analyzers.perplexity import PerplexityAnalyzer
        if not fast:
            analyzers.append(PerplexityAnalyzer())
    except ImportError:
        pass

    results = [a.analyze(text) for a in analyzers]
    result = ensemble.combine(results)
    return result.to_dict()


class VisualizerHandler(SimpleHTTPRequestHandler):
    """HTTP handler for the visualizer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_POST(self):
        if self.path == "/api/analyze":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(body)
                text = data.get("text", "")
                fast = data.get("fast", False)

                if not text.strip():
                    self._json_response({"error": "No text provided"}, 400)
                    return

                result = _analyze(text, fast=fast)
                self._json_response(result)

            except json.JSONDecodeError:
                self._json_response({"error": "Invalid JSON"}, 400)
            except Exception as e:
                self._json_response({"error": str(e)}, 500)
        else:
            self.send_error(404)

    def _json_response(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress request logs unless error
        if args and str(args[1]).startswith("4") or str(args[1]).startswith("5"):
            super().log_message(format, *args)


def run_server(port: int = 7272, open_browser: bool = True):
    """Start the visualizer server."""
    server = HTTPServer(("127.0.0.1", port), VisualizerHandler)
    url = f"http://127.0.0.1:{port}"

    if open_browser:
        import webbrowser
        webbrowser.open(url)

    return server, url
