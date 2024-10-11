#!/usr/bin/env python3
from PIL import Image
from pathlib import Path
import concurrent.futures
import subprocess as sp
import shutil, re

def default_txt():
	s = ''';mode800
*define

caption "処女回路 for ONScripter"

rmenu "Ｓａｖｅ",save,"Ｌｏａｄ",load,"Ｓｋｉｐ",skip,"Ｌｏｇ",lookback,"Ｃｌｏｓｅ",windowerase,"Ｔｉｔｌｅ",reset
;rmenu "セーブ",save,"ロード",load,"リセット",reset

savenumber 18
transmode alpha
globalon
rubyon
saveon
nsa
humanz 10
windowback

numalias videopath,190

effect 10,10,500
;<<-EFFECT->>


defsub msgName

game
;----------------------------------------
;キャラ名中央表示用座標取得
*msgName
	getparam $1

	;文字24px+幅2px=26px
	;len取得数/2=文字数(一文字で2判定っぽい)
	;文字数x28px-2px=名前全体の文字サイズ

	;キャラ名windowの横幅は165px
	;(キャラ名windowの横幅-名前全体の文字サイズ)/2=X座標

	len %1,$1
	mov %2,180+(165/2)-((%1/2)*(24+2)-2)/2

	lsp 1,"data\gui\sys_namebox_bg.png",180,420
	strsp 0,$1,%2,423,7,1,24,24,2,3,0,1
return

;----------------------------------------
*start
setwindow 190,480,24,3,24,24,0,5,15,1,1,"data/gui/sys_textwindow_bg.png",0,343

bg black,1
goto *SYS_MAIN_KS

end
;----------------------------------------
'''
	return s
#--------------------def--------------------
#吉里吉里の命令文及び変数指定をざっくりpythonの辞書に変換するやつ
def krcmd2krdict(c):
	kr_dict = {}

	for p in re.findall(r'([A-z0-9-_]+?)=(["|”|″](.*?)["|”|″]|([^\t\s]+))', c):
		kr_dict[p[0]] = p[2] if p[2] else p[3]

	return kr_dict



# ディレクトリの存在チェック関数
def dir_check(path_list):

	CHK = True
	for p in path_list:
		if not p.exists():
			print('ERROR: "' + str(p) + '" is not found!')
			CHK = False
			
	return CHK


def effect_edit(t,f,effect_startnum,effect_list):

	list_num=0
	if re.fullmatch(r'[0-9]+',t):#timeが数字のみ＝本処理

		for i, e in enumerate(effect_list,effect_startnum+1):#1からだと番号が競合する可能性あり
			if (e[0] == t) and (e[1] == f):
				list_num = i

		if not list_num:
			effect_list.append([t,f])
			list_num = len(effect_list)+effect_startnum

	return str(list_num),effect_startnum,effect_list


#
def image_convert(PATH_DICT):
	pass
	


# txt置換→0.txt出力関数
def text_cnv(DEBUG_MODE, zero_txt, scenario):
	
	#if文変換時に使うgotoの連番 - 一桁はCtrl+F検索時面倒なので10スタート
	if_goto_cnt = 10
	end_goto_cnt = 10

	effect_startnum = 10
	effect_list = []

	#default.txtを読み込み
	txt = default_txt()

	#
	ks_list = [
		{'name':'sys_main.ks', 'encoding':'cp932'},
		{'name':'s_001_prologue.ks', 'encoding':'utf-16'},

	]

	for di in ks_list:
		p = Path(scenario / di['name'])

		#if入った際にelseの行き先とか突っ込んどく - 配列にすることでif内ifに対応
		if_list = []
		end_list = []

		#iscript
		mode_iscript = False

		#シナリオファイルを読み込み
		with open(p, encoding=di['encoding'], errors='ignore') as f: fr = f.read()

		#シナリオ本編専用置換処理 - sys_main相手だとeval内の[0]とかで盛大に破綻するのでそれ回避
		if (not di['name'] == 'sys_main.ks'):
			fr = fr.replace(r'[「]', r'「')
			fr = fr.replace(r'[」]', r'」')
			fr = fr.replace(r'[', '\n[')
			fr = fr.replace(r']', ']\n')

		#デコード済みtxt一つごとに開始時改行&サブルーチン化
		if DEBUG_MODE: txt += '\n;--------------- '+ str(p.parent.name) + ' - ' + str(p.name) +' ---------------'
		txt += ('\n*'+ str(p.name).upper().replace(r'.', r'_') +'\n')

		#行ごとfor
		for line in fr.splitlines():

			#行頭タブ削除
			line = re.sub(r'(\t*)(.*)', r'\2', line)

			#空行ではない場合のみ処理
			if line:
				#スクリプト処理
				if mode_iscript:
					if (line == r'@endscript'):
						mode_iscript = False
						if DEBUG_MODE: txt += (';;' + line + '\n')
					
					else:
						txt += (';;' + line + '\n')#仮
				
				#命令
				elif (line[0] == r'@') or (line[0] == r'['):
					line = line.lower()

					#@時→@消す([1:]) []時→[]消す([1:-1])
					if (line[0] == r'@'): d = krcmd2krdict('kr_cmd=' + line[1:])
					else: d = krcmd2krdict('kr_cmd=' + line[1:-1])

					kr_cmd = d['kr_cmd']
					
					#改ページ
					if (kr_cmd == 'plc'):
						txt += ('\\\n')

					#スクリプト開始
					elif (kr_cmd == 'iscript'):
						mode_iscript = True
						if DEBUG_MODE: txt += (';;' + line + '\n')

					#シナリオ呼び出し
					elif (kr_cmd == 'call'):
						storage = str(d['storage'])
						txt += (r'gosub *' + storage.upper().replace(r'.', r'_') + '\n')
					
					#gosubなどで呼ばれたシナリオ帰る
					elif (kr_cmd == 'return'):
						txt += ('return\n')

					#動画開ける
					elif (kr_cmd == 'openvideo'):
						storage = str(d['storage'])
						txt += (r'mov $videopath,"' + storage.replace('\'', '').replace(r'&system.exepath+', '') + '"\n' )

					#動画再生
					elif (kr_cmd == 'playvideo'):
						txt += (r'mpegplay $videopath' + '\n')

					#待ち
					elif (kr_cmd == 'wait'):
						time = str(d['time'])
						if DEBUG_MODE: time = str(int(int(time)/10))
						txt += (r'wait ' + time + '\n')

					#背景(スプライト管理)
					elif (kr_cmd == 'bg'):
						storage = str(d['storage'])
						txt += (r'lsp 255,"data/bg/' + storage + '.png"\n')

					#背景(スプライト管理)
					elif (kr_cmd == 'イベント絵'):
						storage = str(d['storage'])
						txt += (r'lsp 255,"data/ev/' + storage + '.png"\n')

					#変更
					elif (kr_cmd == 'tra'):
						rule = str(d.get('rule')) if d.get('rule') else 'fade'
						time = str(d.get('time')) if d.get('time') else '1000'
						s1, effect_startnum, effect_list = effect_edit(time, rule, effect_startnum, effect_list)
						txt += ('print '+ s1 + '\n')

					#名前欄
					elif (kr_cmd == 'name'):
						name = str(d['name'])
						txt += ('msgName "' + name + '"\n')

					#名前欄消す
					elif (kr_cmd == 'x'):
						txt += ('csp 0:csp 1\n')

					#bgm
					elif (kr_cmd == 'bgm'):
						storage = str(d['storage'])
						txt += (r'bgm "data/bgm/' + storage + '.ogg"\n')

					#音楽停止
					elif (kr_cmd == '音楽停止'):
						txt += ('bgmstop\n')

					#voice
					elif (kr_cmd == 'voice'):
						storage = str(d['storage'])
						txt += (r'dwave 1,"data/voice/' + storage + '.ogg"\n')

					#効果音 - 待ち用に関数作って飛ばす、関数先ではresettimer
					elif (kr_cmd == '効果音'):
						storage = str(d['storage'])
						pass #仮

					#効果音停止
					elif (kr_cmd == '効果音停止'):
						pass #仮

					#効果音停止待ち
					elif (kr_cmd == '効果音停止待ち'):
						pass #仮





					#その他 - とりあえず表示(多分ない)
					else:
						print(d)#, line)
						txt += (';' + line + '\n')

				#元々コメントアウト - デバッグ時強調、通常時非表示
				elif (line[0] == r';'):
					if DEBUG_MODE: txt += (';;;;' + line + '\n')

				#krkr側ラベル - とりあえずコメントアウト
				elif (line[0] == r'*'):
					txt += (';' + line + '\n')

				#命令以外
				else:
					#max27
					txt += (line + '\n')
		
		#シナリオそのまま終わってgoto先無いとき用
		txt += ('\nreset')
		
		#ifスタック消費しきってない場合バグなので表示
		if if_list != []: print('ERROR: if_conv ',if_list)
	
	
	add0txt_effect = ''
	for i,e in enumerate(effect_list,effect_startnum+1):#エフェクト定義用の配列を命令文に&置換
		if e[1] == 'fade':
			add0txt_effect +='effect '+str(i)+',10,'+e[0]+'\n'
		else:
			add0txt_effect +='effect '+str(i)+',18,'+e[0]+',"data/rule/'+str(e[1]).replace('"','')+'.png"\n'
	txt = txt.replace(r';<<-EFFECT->>', add0txt_effect)


	#出力結果を書き込み
	open(zero_txt, 'w', errors='ignore').write(txt)

	return



# メイン関数
def main():

	# デバッグモード
	debug = 1

	#同一階層のパスを変数へ代入
	same_hierarchy = Path.cwd()

	#デバッグ時はtestディレクトリ直下
	if debug: same_hierarchy = (same_hierarchy / '_test')


	#デバッグ用自動展開(本当は通常利用向けにも実装したほうがいいんだが…)
	if debug:
		td = (Path.cwd()/ '_test' / 'data')
		pv = (Path.cwd()/ '_test' / '処女回路PV.wmv')

		if not td.exists():
			td.mkdir(parents=True)
			sp.run([r'C:\_software\_zisaku\NSC2ONS4PSP\tools\Garbro_console\GARbro.Console.exe',
				 'x', '-if', 'png', '-ca', '-o', td,
				 r'D:\__game_tmp\otome_c_trial\処女回路_体験版\data.xp3'], shell=True )
		if not pv.exists():
			shutil.copy(r'D:\__game_tmp\otome_c_trial\処女回路_体験版\処女回路PV.wmv', pv)
		
	
	#利用するパスを辞書に入れ一括代入
	PATH_DICT = {
		#先に準備しておくべきファイル一覧
		'data' :(same_hierarchy / 'data'),
		'bg' :(same_hierarchy / 'data' / 'bg'),
		'bgm' :(same_hierarchy / 'data' / 'bgm'),
		'ev' :(same_hierarchy / 'data' / 'ev'),
		'face' :(same_hierarchy / 'data' / 'face'),
		'gui' :(same_hierarchy / 'data' / 'gui'),
		'rule' :(same_hierarchy / 'data' / 'rule'),
		'scenario' :(same_hierarchy / 'data' / 'scenario'),
		'se' :(same_hierarchy / 'data' / 'se'),
		'stand' :(same_hierarchy / 'data' / 'stand'),
		'voice' :(same_hierarchy / 'data' / 'voice'),
		
	}

	PATH_DICT2 = {
		#変換後に出力されるファイル一覧
		'0_txt' :(same_hierarchy / '0.txt'),
	}

	#デバッグ用いろいろ
	if debug:
		if Path(same_hierarchy / 'stderr.txt').exists():Path(same_hierarchy / 'stderr.txt').unlink()
		if Path(same_hierarchy / 'stdout.txt').exists():Path(same_hierarchy / 'stdout.txt').unlink()
		if Path(same_hierarchy / 'envdata').exists():Path(same_hierarchy / 'envdata').unlink()
		if Path(same_hierarchy / 'gloval.sav').exists():Path(same_hierarchy / 'gloval.sav').unlink()

	#ディレクトリの存在チェック
	dir_check_result = dir_check(PATH_DICT.values())

	#存在しない場合終了
	if not dir_check_result: return

	#一部画像変換
	image_convert(PATH_DICT)

	#txt置換→0.txt出力
	text_cnv(debug, PATH_DICT2['0_txt'], PATH_DICT['scenario'])

	#不要ファイル削除
	#if not debug: shutil.rmtree(PATH_DICT['data'])


main()


#KIRIKIRI2ONS_Moviendo-otomec


#パッチ修正箇所:s_001_prologue.ks
#間接 → 関節

#[x] 文字前 →name消去?