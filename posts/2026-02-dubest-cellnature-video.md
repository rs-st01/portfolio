---
title: "ドゥベスト セルナチュレLP用 AIイメージ動画制作"
client: "ドゥベスト"
period: "2026-01 ~ 2026-02"
purpose: "セルナチュレLPに掲載するイメージ動画をAI動画生成で制作"
ai_tools:
  - nanobananaPro
  - Adobe Firefly
  - Google AI Studio
  - Gemini
  - Premiere Pro
summary: "AI動画生成で4本のイメージ動画を制作。開始・終了フレームから中間の動きをAIで生成"
date: 2026-02-13
order: 3
tags:
  - 動画生成
  - LP
  - 化粧品
---

## この事例のポイント

ドゥベストのセルナチュレLPに掲載するイメージ動画を、**AI動画生成ツール** を使って制作した事例です。

従来、こうしたイメージ動画は実写撮影やモーショングラフィックスで制作するのが一般的で、コスト・時間ともにそれなりにかかるものでした。今回は **AIで静止画から動画を生成する** という手法で、4本のイメージ動画を制作しました。

## 制作した動画

以下の4本を制作しました。

### 1. 質感イメージ

<video controls muted loop playsinline width="100%">
  <source src="../video/lfeeling_movie.mp4" type="video/mp4">
</video>

### 2. パールの輝き

<video controls muted loop playsinline width="100%">
  <source src="../video/pearl_movie.mp4" type="video/mp4">
</video>

### 3. パウダー

<video controls muted loop playsinline width="100%">
  <source src="../video/powder.mp4" type="video/mp4">
</video>

### 4. 使用イメージ

<video controls muted loop playsinline width="100%">
  <source src="../video/wogata_movie.mp4" type="video/mp4">
</video>

## 制作ワークフロー

### ステップ1：静止画の作成（nanobananaPro）

まず **nanobananaPro** で、動画の **開始フレーム** と **終了フレーム** にあたる静止画を作成します。ここで動画の構図・色味・雰囲気のベースが決まります。

### ステップ2：AI動画生成（Adobe Firefly / Google AI Studio）

作成した開始・終了フレームの静止画をもとに、**間の動き** をAI動画生成ツールで生成します。主に以下の2つを使用しました。

- **Adobe Firefly** — 動画AIモデル
- **Google AI Studio** — GoogleのAI動画生成

### ステップ3：プロンプト最適化（Gemini）

動きが思い通りにいかないケースが多く、**1シーンあたり10本以上** の試作を繰り返すことになりました。

ただし制作期間中、幸運にも **Firefly の動画AIモデルのクレジット消費が無料** になっており、さらに **AI Studio で3万円分のクレジットプレゼント** があったため、実質作り放題の状態でした。この恩恵を最大限に活かし、**Gemini にプロンプトを書かせて最適化** することで、最終的に満足のいく仕上がりにたどり着きました。

### ステップ4：編集・テロップ（Premiere Pro）

生成した動画素材を **Premiere Pro** でつなぎ合わせ、テロップを入れて完成です。

## 成果

- 実写撮影・モーショングラフィックス制作なしで、LP用のイメージ動画4本を制作
- 静止画→動画という新しいワークフローを確立
- クレジット無料期間を活用し、大量試作によるクオリティ追求が可能だった
- Geminiでのプロンプト最適化により、AI動画生成の精度向上ノウハウを蓄積

## 再利用可能ポイント

- **開始・終了フレームを静止画で作り、間をAI生成** という手法は他の商品LPにも応用可能
- Gemini によるプロンプト最適化の知見は、今後の動画生成案件に転用できる
- nanobananaPro で高品質な静止画を作れれば、動画のクオリティも底上げされる

## 課題・改善点

- 動きの制御が難しく、1シーンあたり10本以上の試作が必要だったため、かなりの時間を要した
- 今後は **ローカルAI でクレジットを気にせず大量試作する** か、**より制御性の高い動画生成サービスを探す** かの二択で検討中
- テロップ入れなど最終編集は手作業（Premiere Pro）が必要
