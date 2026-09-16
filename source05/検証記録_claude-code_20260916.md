# Claude Code 検証記録｜2026-09-16

HANDOFF.md の手順を Claude Code（Fable 5.1・macOS・Python 3.8.2）で再現した記録。観客向け画面には載せない制作メモ。

## 結果

- `python3 source05/build.py` は成功。生成された `sessions/05/index.html` はコミット済みと完全一致（git status にdiffなし）。
- `python3 -m http.server 8766` で配信し、内蔵ブラウザ 1440×810 で16枚すべてを確認。ステージ外へのはみ出し要素なし。
- 年1/3/5%切り替え → 利息 1万/3万/5万円、バーは20/60/100%。
- 質問ページ：右矢印1回目で答えが開き、2回目で次ページへ進む。
- 市場金利ボタン：金利↑・既発債価格↓、「元に戻す」で→/→に戻る。
- 章ボタン・前後ボタン・全画面ボタン動作。JSエラー0、素材404なし（PNGは200）。

## この環境でできること・できないこと

| 作業 | Claude Code | 備考 |
|---|---|---|
| 文章・構成・CSS・JSの編集（build.py） | ○ | 編集元→再生成→ブラウザ実機確認まで一貫 |
| 実ブラウザでの折り返し・はみ出し・操作確認 | ○ | 内蔵ブラウザでスクリーンショットとJS検査 |
| SVG/CSSによる図・アニメーション・光の演出 | ○ | 現在の `.currents` と同方式 |
| データからのグラフ生成（価格系列・金利推移） | ○ | 歴史ページの肉付けに向く。SVGで生成しHTMLへ埋め込み |
| 写実的な静止画（トップ背景など）の生成 | × | 画像生成ツールなし。ChatGPT・Google Flow等で作成 |
| 動画素材の生成 | × | 同上。`video`要素の実装側はこちらで可 |
| manifest更新・commit・push | ○ | pushは指示があるときのみ |

## 画像の受け渡し方式（HANDOFFの「別レイヤー」方式をそのまま使う）

1. 外部ツールで 16:9・文字なし・左半分は暗い余白・紺と金/青緑 の画像を作る。
2. `sessions/05/assets/rate05/` に新しい名前で保存（例 `interest-city-v2.png`）。
3. `source05/build.py` の `.city` の `background:url(...)` を新しい名前に変更して再生成。
4. `source05/画像生成記録.json` に生成元・プロンプト・ファイル名を追記。
5. ブラウザで `background-size:cover` の切れ方と文字の重なりを確認。

## 用途別の分担（案）

- 第一印象を決める背景・情景 → 外部生成（ChatGPT / Google Flow）。Claude はプロンプト草案と受け入れ確認を担当。
- 仕組みの図・比較図・数値の動き・歴史の価格系列 → Claude が SVG/CSS/JS で生成。写真的素材は不要。
- 質問の開閉・切り替え・ナビゲーション → Claude が build.py で実装・検証。

## 備考

- `build.py` 最終行の `write_text(html)` はエンコーディング未指定。今回のmacOS環境ではUTF-8で書けたが、他環境では `encoding='utf-8'` の明示が安全。
- ローカルの `Claude(alpha)/mirai-seminar-slides` は元環境（GPT側）の作業リポジトリで公開リポジトリとは履歴が別。公開側の作業は `mirai-seminar-slides-public` で行う。
