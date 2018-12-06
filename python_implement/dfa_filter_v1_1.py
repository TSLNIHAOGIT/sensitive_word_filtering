import time
time1=time.time()
# 中文DFA算法过滤敏感词改进版本
class Chinese_DFAFilter():
    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def add(self, keyword):
        keyword = keyword.lower()
        chars = keyword.strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    # def parse(self, path):
    #     with open(path,encoding='utf-8') as f:
    #         for keyword in f:
    #             # print(keyword)
    #             self.add(str(keyword).strip())

    # 加载敏感词函数#原来的加载
    def parse(self, data):
        for i in data['lable']:
            self.add(str(i).strip())

    def parse(self, path):
        with open(path,encoding='utf-8') as f:
            for keyword in f:
                self.add(str(keyword).strip())

    def filter(self, message, repl="*"):
        message = message.lower()
        ret = []
        start = 0
        hit_word=[]
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        # print(step_ins)
                        ret.append(repl * step_ins)
                        # print("%s--------step_ins" %step_ins)
                        start += step_ins - 1
                        # print("%s--------start" %start)
                        kk=message[start-step_ins+1:start+1]
                        hit_word.append(kk)
                        break
                else:
                    ret.append(message[start])
                    # print(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return hit_word
if __name__=='__main__':

    gfw = Chinese_DFAFilter()
    path = "/Users/ozintel/Downloads/网站敏感词检测/网站敏感词库/dictionaries/chinese_dictionary.txt"
    gfw.parse(path)
    text = "新疆骚乱苹果新品发布会傻逼"
    result = gfw.filter(text)

    print(text)
    print(result)
    time2 = time.time()
    print('总共耗时：' + str(time2 - time1) + 's')

