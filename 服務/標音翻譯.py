from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
from 臺灣言語工具.解析整理.文章粗胚 import 文章粗胚
from django.http.response import HttpResponse
from 臺灣言語工具.翻譯.斷詞斷字翻譯 import 斷詞斷字翻譯
from 臺灣言語工具.翻譯.摩西工具.摩西用戶端 import 摩西用戶端
from 臺灣言語工具.音標系統.官話.官話注音符號 import 官話注音符號
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.翻譯.摩西工具.語句編碼器 import 語句編碼器
from 臺灣言語工具.斷詞.中研院工具.官方斷詞剖析工具 import 官方斷詞剖析工具
from 臺灣言語工具.語音合成.句物件轉合成標仔 import 句物件轉合成標仔
import htsengine
import os
from 臺灣言語工具.語音合成.音檔頭前表 import 音檔頭前表
import gzip
import pickle
from 臺灣言語工具.表單.肯語句連詞 import 肯語句連詞
from 臺灣言語工具.斷詞.拄好長度辭典揣詞 import 拄好長度辭典揣詞
from 臺灣言語工具.斷詞.連詞揀集內組 import 連詞揀集內組
from 臺灣言語工具.解析整理.轉物件音家私 import 轉物件音家私
import time
import Pyro4

_粗胚 = 文章粗胚()
_分析器 = 拆文分析器()
_家私 = 轉物件音家私()

_揣詞 = 拄好長度辭典揣詞()
_揀集內組 = 連詞揀集內組()

Pyro4.config.SERIALIZER = 'pickle'
閩南語辭典 = Pyro4.Proxy("PYRO:閩南語辭典@localhost:9092")
閩南語連詞 = 肯語句連詞('語料/翻譯/閩.lm')#Pyro4.Proxy("PYRO:閩南語連詞@localhost:9092")

_斷詞斷字翻譯 = 斷詞斷字翻譯()
_官方斷詞剖析工具 = 官方斷詞剖析工具()
_編碼器 = 語句編碼器()
斷詞用戶端 = 摩西用戶端('localhost', 8105, 編碼器=_編碼器)
斷字用戶端 = 摩西用戶端('localhost', 8205, 編碼器=_編碼器)
_句物件轉合成標仔 = 句物件轉合成標仔()

def 閩南語標音物件(腔口, 語句):
	print('語句', 語句)
	處理減號 = _粗胚.建立物件語句前處理減號(臺灣閩南語羅馬字拼音, 語句)
	章物件 = _分析器.建立章物件(處理減號)
	標準章物件 = _家私.轉音(臺灣閩南語羅馬字拼音, 章物件)
	斷好, 分數, 詞數 = _揣詞.揣詞(閩南語辭典, 標準章物件)
	標好, 分數, 詞數 = _揀集內組.揀(閩南語連詞, 斷好)
	return 標好

def 閩南語翻譯物件(腔口, 語句):
	print('語句', 語句)
	try:
		斷詞物件 = _官方斷詞剖析工具.斷詞(語句)
		print('斷詞物件', 斷詞物件)
		處理減號 = _粗胚.建立物件語句前處理減號(官話注音符號, 語句)
		print('處理減號', 處理減號)
		華語章物件 = _分析器.建立章物件(處理減號)
		print('華語章物件', 華語章物件)
		閩南語章物件 = _斷詞斷字翻譯.譯(斷詞用戶端, 斷字用戶端, 華語章物件)
	except:
		print('斷詞失敗')
		處理減號 = _粗胚.建立物件語句前處理減號(官話注音符號, 語句)
		print('處理減號', 處理減號)
		華語章物件 = _分析器.建立章物件(處理減號)
		print('華語章物件', 華語章物件)
		閩南語章物件 = _斷詞斷字翻譯.譯(斷字用戶端, 斷字用戶端, 華語章物件)
	return 閩南語章物件
_音檔頭前表 = 音檔頭前表()
def 章物件轉標仔(標仔陣列):
# 	for a in 標仔陣列[:5]:
# 		print('a', a)
	愛合成標仔 = _句物件轉合成標仔.跳脫標仔陣列(標仔陣列)
	模型 = 'HTSLSPtan5tso5.htsvoice'
	一點幾位元組, 一秒幾點, 幾个聲道, 原始取樣 = \
		htsengine.synthesize(模型, 愛合成標仔)
	聲音檔 = _音檔頭前表.加起哩(原始取樣, 一點幾位元組, 一秒幾點, 幾个聲道)
	回應 = HttpResponse()
	回應.write(聲音檔)
	回應['Content-Type'] = 'audio/wav'
	回應['Content-Disposition'] = 'attachment; filename=a.wav'
	回應['Content-Length'] = len(聲音檔)
	return 回應
