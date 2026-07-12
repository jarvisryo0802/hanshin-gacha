#!/bin/zsh
# カードを追加・変更したら、これをダブルクリックするだけでネット公開版が更新されます
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$PATH"

python3 - << 'EOF'
import os
import shutil
from server import build_cards_js

DST = 'docs'
shutil.rmtree(DST, ignore_errors=True)
os.makedirs(DST)

for f in ['index.html', 'sw.js', 'manifest.webmanifest', 'icon-180.png', 'icon-512.png']:
    shutil.copy(f, DST)
shutil.copytree('cards', os.path.join(DST, 'cards'), ignore=shutil.ignore_patterns('.*'))

with open(os.path.join(DST, 'cards.js'), 'w', encoding='utf-8') as fp:
    fp.write(build_cards_js())
open(os.path.join(DST, '.nojekyll'), 'w').close()

n = len([f for f in os.listdir(os.path.join(DST, 'cards')) if not f.startswith('.')])
print(f'✅ 公開ファイルを準備しました(カード {n} まい)')
EOF

git add -A
git commit -m "カードを更新" > /dev/null 2>&1 || true
git push

echo ""
echo "=============================================="
echo "  ✅ 公開しました!(反映まで1〜2分)"
echo "  📱 https://jarvisryo0802.github.io/hanshin-gacha/"
echo "=============================================="
echo ""
