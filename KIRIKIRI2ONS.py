import subprocess as sp
from pathlib import Path
import shutil


def main():



	data = (Path.cwd()/ 'data')




	if data.exists():shutil.rmtree(data)
	data.mkdir()

	#自動展開 - デバッグ用(本当は通常利用向けに実装したほうがいいんだが…)
	sp.run([r'C:\_software\_zisaku\NSC2ONS4PSP\tools\Garbro_console\GARbro.Console.exe',
		 'x', '-if', 'png', '-ca', '-o', data,
		 r'D:\__game_tmp\otome_c_trial\処女回路_体験版\data.xp3'], shell=True )

#KIRIKIRI2ONS_Moviendo-otomec


#パッチ修正箇所:s_001_prologue.ks
#間接 → 関節

main()