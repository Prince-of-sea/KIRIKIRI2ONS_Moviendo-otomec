# KIRIKIRI2ONS_Moviendo-otomec

## なにこれ
  2011年にMoviendo様から発売された、18禁PC向けノベルゲーム'[処女回路](https://web.archive.org/web/20160730000957fw_/http://www.moviendo-soft.com:80/otm_s/top.php)'を<br>
  ONScripter形式へ変換するためのコンバータです<br>

## 再現度
原作との主な違いは以下
 - 立ち絵の重なり順が違う&Y座標(=縦移動)がうまく動いてなさそう ※X座標(=横移動)はほぼ正常
 - 左下の顔画像表示がかなり適当、更新されなかったりそもそも出なかったり
 - キャラの移動とメッセージ表示進行が同時に行えない(ONSの仕様)
 - その他一部演出/セーブ/ロード/設定画面などは超簡略化
 - スタッフロールが若干原作と違う
 - 全体的に改行がズレ気味
 - ギャラリー未実装
 - 独自機能としてHシーンスキップ機能を(勝手に)実装
    - なおこの機能、シーン途中の選択肢も関係なく飛ばすため<br>
      好感度が足りずに特定ルートに入れなくなる、なんてこともあるようです<br>
      おまけ程度のものだと考えてください<br>


いつにも増してガバガバです<br>
このゲームめちゃくちゃ立ち絵よく動くからONSでの再現大変なんですよねぇ…(言い訳)<br>

## 使い方
 1. 適当な作業フォルダを作成
 2. [GARBro](https://drive.google.com/file/d/1gH9nNRxaz8GexN0B1hWyUc3o692bkWXX/view)で**patch.xp3を除く**(そもそもない場合は無視)すべてのxp3を作業フォルダへ展開<br>

     設定は以下の通り↓<br>
     ![](image1.png)

 3. 展開先のディレクトリで[このコンバータ](https://github.com/Prince-of-sea/KIRIKIRI2ONS_Moviendo-otomec/releases/latest)をDL/起動させ変換(一瞬で終わります)<br>
    変換前の時点で以下のような構成になっていればOKです↓<br>
```
C:.
│  KIRIKIRI2ONS_Moviendo-otomec.exe
│  
├─bg
│      bg_並木_夕.png
│      (～略)
│      bg_風呂2_暗.png
│      
├─bgm
│      bgm_ed.ogg
│      (～略)
│      bgm_s_04.ogg
│      
├─data
│  │  startup.tjs
│  │  
│  └─system
│          AfterInit.tjs
│          (～略)
│          YesNoDialog.tjs
│          
├─ev
│      ev_0_0.png
│      (～略)
│      ev_9_2.png
│      
├─face
│      face_ali_1_h_微笑.png
│      (～略)
│      face_sal_2_y_考.png
│      
├─fg
│      fg_effect_hikari_1.png
│      (～略)
│      fg_effect_魔方陣1.png
│      
├─gui
│      font12px.tft
│      (～略)
│      _sys_title_btani_a.png
│      
├─rule
│      rule_3d_ガラス.png
│      (～略)
│      rule_高速接近2.png
│      
├─scenario
│      first.ks
│      (～略)
│      s_003_end_sala.ks
│      
├─se
│      SE11.ogg
│      (～略)
│      _sys_se_onenter2.wav
│      
├─stand
│      stand_ali_1_h_微笑.png
│      (～略)
│      stand_tb_sal_2_y_考.png
│      
└─voice
        ALI_A1_001.ogg
        (～略)
        SAL_A1_799.ogg
```
 4. ウィンドウが消え、0.txtができれば完成<br>
    exe等の不要データを削除し、変換済みファイルと共に利用ハードへ転送

## 注意事項
 - 当然ですが公式ツールではありません
 - __パッケージ版で動作確認しています__ その他の動作は未確認
 - 本ツールの使用において生じた問題や不利益などについて、作者は一切の責任を負いません
 - 制作サークル様に迷惑をかけたくないので、<br>
   本ツールのSNS等での拡散は**ご遠慮ください**<br>
   ~~(拡散されるほどのツールでもない気はするが一応)~~<br>

## その他
本作の変換を追加でサポートする[PSP向け自動変換ツール作ってます](https://github.com/Prince-of-sea/ONScripter_Multi_Converter)<br>
もしPSPで遊ぶ場合はぜひご利用ください(v1.4.8以上推奨)