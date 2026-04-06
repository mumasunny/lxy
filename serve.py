#!/usr/bin/env python3
"""
在本目录启动一个静态文件服务，并把 POST /proxy/xhs/detail 转发到 XHS-Downloader
（默认 http://127.0.0.1:5556/xhs/detail），解决浏览器跨域问题。

用法：
  cd xhs-standalone
  python serve.py

然后浏览器打开终端里提示的地址（例如 http://127.0.0.1:8765/）。
请先另开终端在 XHS-Downloader 目录执行：python main.py api
"""
from __future__ import annotations

import http.client
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 8765
XHS_HOST = "127.0.0.1"
XHS_PORT = 5556
XHS_PATH = "/xhs/detail"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def log_message(self, fmt, *args_):
        sys.stderr.write("%s - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), fmt % args_))

    def do_OPTIONS(self):
        if self.path == "/proxy/xhs/detail" or self.path.startswith("/proxy/xhs/detail?"):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
            return
        super().do_OPTIONS()

    def do_POST(self):
        if self.path != "/proxy/xhs/detail":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b'{"detail":"Invalid JSON body"}')
            return

        conn = http.client.HTTPConnection(XHS_HOST, XHS_PORT, timeout=300)
        try:
            conn.request(
                "POST",
                XHS_PATH,
                body=body,
                headers={"Content-Type": "application/json"},
            )
            resp = conn.getresponse()
            data = resp.read()
        except OSError as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            msg = json.dumps({"detail": f"无法连接 XHS-Downloader ({XHS_HOST}:{XHS_PORT}): {e}"})
            self.wfile.write(msg.encode())
            return
        finally:
            conn.close()

        self.send_response(resp.status)
        self.send_header("Access-Control-Allow-Origin", "*")
        ct = resp.getheader("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Type", ct)
        self.end_headers()
        self.wfile.write(data)


def main():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"打开浏览器: http://{HOST}:{PORT}/index.html")
    print("（确保已运行: python main.py api  在 XHS-Downloader 目录）")
    print("按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")


if __name__ == "__main__":
    main()
