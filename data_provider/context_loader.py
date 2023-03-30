from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import math

stp = stopwords.words('english')


class ContextLoader:
    def __init__(self, docu, tf_norm_factor=1.2, doc_len_pun=0.75) -> None:
        self.para_list, self.ctr_list, self.len_list, self.base_ctr = self._split_doc(
            docu)
        self.avgdl = sum(self.len_list)/len(self.len_list)
        self.tf_norm_factor = tf_norm_factor
        self.doc_len_pun = doc_len_pun

    def _split_doc(self, docu):
        para_list = docu.split('\n\n')
        len_list = []
        ctr_list = []
        out_para = []
        base_ctr = Counter()
        for para in para_list:
            para = para.strip().lower()
            if len(para) == 0:
                continue
            out_para.append(para)
            wlist = word_tokenize(para)
            len_list.append(len(wlist))
            tmp_ctr = Counter(wlist)
            ctr_list.append(tmp_ctr)
            for k, v in tmp_ctr.items():
                base_ctr[k] += v

        return out_para, ctr_list, len_list, base_ctr

    def retrieve(self, question, answer):
        # input_word = question+" "+answer
        input_word = (question+" "+answer).lower()
        k_plus_1 = self.tf_norm_factor+1
        # wlist = [w for w in word_tokenize(input_word)]
        wlist = [w for w in word_tokenize(input_word) if w not in stp]
        idf_list = [self._idf(w) for w in wlist]
        score_list = []
        for i, para_ctr in enumerate(self.ctr_list):
            deno = self.tf_norm_factor * \
                (1-self.doc_len_pun+self.doc_len_pun *
                 (self.len_list[i]/self.avgdl))
            tmp_score = 0
            for j, w in enumerate(wlist):
                w_tf = para_ctr[w]
                w_score = idf_list[j]*w_tf*k_plus_1/(w_tf+deno)
                # if w_score < 0:
                #     print(w_score)
                tmp_score += w_score
            score_list.append((i, tmp_score))
        para_id_ranked_list = sorted(
            score_list, key=lambda it: it[1], reverse=True)
        para_ranked = [(self.para_list[it[0]], it[1])
                       for it in para_id_ranked_list]
        return para_ranked

    def _idf(self, w):
        N = len(self.ctr_list)
        n = sum([min(1, ctr[w]) for ctr in self.ctr_list])
        idf = math.log(1+(N-n+0.5)/(n+0.5))
        if idf < 0:
            print(w, '\t', idf, '\t', n, '\t', N)
        return idf
