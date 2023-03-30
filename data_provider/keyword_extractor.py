from collections import Counter, defaultdict
from nltk import word_tokenize
from nltk.corpus import stopwords
import sys

english_punctuations = {',', '.', ':', ';', '?',
                        '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%'}
stp = stopwords.words('english')


class KeywordExtractor:
    def __init__(self, docu, iter=10, ngram=2, d=0.85, window=5) -> None:
        self.ngram = ngram
        self.iter = iter
        self.d = d
        self.window = window
        self.graph = defaultdict(lambda: defaultdict(list))
        self.weight_map = dict()
        self.plist, self.wlist = self._clean_docu(docu)
        self._build_graph()

    def _clean_docu(self, docu):
        para_list = [p for p in docu.split('\n\n') if len(p.strip()) > 0]
        w_list = []
        for p in para_list:
            tmp_wlist = [
                w for w in word_tokenize(p)
                if w.lower() not in stp and
                w not in english_punctuations]
            # taged_wlist = pos_tag(tmp_wlist)
            w_list.append([' '.join(tmp_wlist[i:i+self.ngram])
                          for i in range(len(tmp_wlist) + 1-self.ngram)])
        return para_list, w_list

    def _build_graph(self):
        cm = Counter()
        for pid, pwlist in enumerate(self.wlist):
            for i, w in enumerate(pwlist):
                for j in range(i+1, min(i+self.window+1, len(pwlist))):
                    cm[(w, pwlist[j])] += 1
            for wp, freq in cm.items():
                self.graph[pid][wp[0]].append((wp[0], wp[1], freq))
                self.graph[pid][wp[1]].append((wp[1], wp[0], freq))

    def num_paragraph(self):
        return len(self.plist)

    def get_paragraph(self, pid):
        return self.plist[pid]

    def get_keywords(self, pid):
        if pid in self.weight_map:
            return self.weight_map[pid]
        ws = defaultdict(float)
        pgraph = self.graph[pid]
        outSum = defaultdict(float)

        wsdef = 1.0 / (len(pgraph) or 1.0)
        for n, out in pgraph.items():
            ws[n] = wsdef
            outSum[n] = sum((e[2] for e in out), 0.0)

        sorted_keys = sorted(pgraph.keys())
        for _ in range(self.iter):
            for n in sorted_keys:
                s = 0
                for e in pgraph[n]:
                    s += e[2] / outSum[e[1]] * ws[e[1]]
                ws[n] = (1 - self.d) + self.d * s

        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])

        for w in ws.values():
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w

        for n, w in ws.items():
            ws[n] = (w - min_rank / 10.0) / (max_rank - min_rank / 10.0)

        w_rank = sorted(ws.items(), key=lambda it: it[1], reverse=True)
        self.weight_map[pid] = w_rank
        return w_rank


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--doc')
    args = parser.parse_args()

    with open(args.doc, 'r') as f:
        doc_content = f.read()

    ext = KeywordExtractor(doc_content)
    pnum = ext.num_paragraph()
    print('Number of valid paragraph: ', pnum)

    while True:
        try:
            pid = int(input('Paragraph id: '))
            print(ext.get_keywords(pid-1), '\n')
        except KeyboardInterrupt:
            break
