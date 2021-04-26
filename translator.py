import requests
import random
from lxml import etree

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


class Translator(object):
    POS = {
        'n.': '名词',
        'pron.': '代词',
        'adj.': '形容词',
        'adv.': '副词',
        'v.': '动词',
        'num.': '数词',
        'art.': '冠词',
        'prep.': '介词',
        'conj.': '连词',
        'interj.': '感叹词',
        'int.': '感叹词',
        'abbr.': '(略)略语',
        'vt.': '及物动词',
        'vi.': '不及物动词'
    }

    FULL_POS = {
        'noun': '名词',
        'pronoun': '代词',
        'adjective': '形容词',
        'adverb': '副词',
        'verb': '动词',
        'numeral': '数词',
        'article': '冠词',
        'preposition': '介词',
        'conjunction': '连词',
        'interjection': '感叹词',
        'abbreviation': '(略)略语'
    }

    def __init__(self, word, max_retry=10):
        super(Translator, self).__init__()
        self.word = word
        self.max_retry = max_retry

    def run(self):
        for _ in range(self.max_retry):
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,pt;q=0.6',
                'Connection': 'keep-alive',
                'Host': 'dict.youdao.com',
                'User-Agent': random.choice(user_agent_list)}
            try:
                resp = requests.get(
                    url=f'http://dict.youdao.com/w/{self.word}/', headers=headers, allow_redirects=True, timeout=10)
                if resp.ok:
                    if '您要找的是不是' in resp.text:
                        return None
                    selector = etree.HTML(resp.text)
                    # 音标
                    phonetics = selector.xpath(
                        '//span[@class="phonetic"]/text()')
                    phonetics = self.phonetic(phonetics)
                    # 词意
                    explains = selector.xpath(
                        '//div[@class="trans-container"]/ul/li/text()')
                    explains = self.explain(explains)
                    return {
                        "phonetics": phonetics,
                        "explains": explains
                    }
            except Exception as e:
                print(e)

    def phonetic(self, phonetics):
        return {"uk": phonetics[0], "us": phonetics[1]} if len(phonetics) >= 2 else {"uk": "", "us": ""}

    def explain(self, explains):
        return [explain.strip() for explain in explains for part in self.POS.keys() if part in explain]


if __name__ == '__main__':
    wt = Translator('whisper')
    print(wt.run())
