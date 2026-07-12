#!/usr/bin/env python3
"""はんしんカードガチャ用のかんたんサーバー。

cards フォルダの画像を自動で読み取って cards.js として配信するので、
画像を入れ直したらブラウザを再読み込みするだけでカードが増えます。
"""
import json
import os
import re
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = 8425
CARDS_DIR = 'cards'
EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.svg', '.heic'}
PREFIX = re.compile(r'^(UR|SR|R|N)[_＿\-](.+)$', re.IGNORECASE)


def build_cards_js():
    cards = []
    if os.path.isdir(CARDS_DIR):
        for f in sorted(os.listdir(CARDS_DIR)):
            base, ext = os.path.splitext(f)
            if f.startswith('.') or ext.lower() not in EXTS:
                continue
            m = PREFIX.match(base)
            if m:
                rarity, name = m.group(1).upper(), m.group(2)
            else:
                rarity, name = 'N', base
            cards.append({'file': f'{CARDS_DIR}/{f}', 'name': name, 'rarity': rarity})
    return 'window.CARD_DATA = ' + json.dumps(cards, ensure_ascii=False) + ';'


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/cards.js':
            body = build_cards_js().encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, *args):
        pass  # ログを静かに


def local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return '127.0.0.1'


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ip = local_ip()
    print()
    print('=' * 46)
    print('  ⚾ はんしんカードガチャ サーバー起動中!')
    print('=' * 46)
    print()
    print(f'  Mac で見る    → http://localhost:{PORT}')
    print(f'  iPhone で見る → http://{ip}:{PORT}')
    print()
    print('  ※ iPhone は Mac と同じ Wi-Fi につないでね')
    print('  ※ やめるときは このウィンドウを閉じる か Ctrl+C')
    print()
    ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
