import os

import pandas as pd
from context_loader import ContextLoader

DOC_ID = 'document_id'
CTX = 'context'
QUE = 'question'
ANS = 'answer'
DIFF = 'difficulty'


class QALoader:
    def __init__(self,
                 homedir,
                 docdir='docs',
                 sheetname='question_answer_pair.csv',
                 topk_para=1) -> None:
        self.homedir = homedir
        self.docdir = docdir
        self.sheetname = sheetname
        self.topk_para = topk_para
        self._prepare()

    def _prepare(self):
        self.sheetpath = os.path.join(
            self.homedir,
            self.sheetname
        )
        self.sheet_df = pd.read_csv(self.sheetpath, index_col=0)

    def loc(self, idx):
        df_row = self.sheet_df.loc[idx]
        doc_path = os.path.join(self.homedir, self.docdir, df_row[DOC_ID][1:])
        out_dict = df_row.to_dict()
        del out_dict[DOC_ID]
        with open(doc_path, 'r') as f:
            ctx_full = f.read()
        cl = ContextLoader(ctx_full)
        para_ranked = cl.retrieve(out_dict[QUE], out_dict[ANS])
        if len(para_ranked) < 1:
            return None
        out_dict[CTX] = [p[0] for p in para_ranked[:self.topk_para]]
        return out_dict

    def shape(self):
        return self.sheet_df.shape


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--home', default='./hwqa')
    args = parser.parse_args()

    dl = QALoader(args.home)

    sheetsize = dl.shape()[0]

    aid = 5
    art_dict = dl.loc(aid)

    print('Question: ', art_dict[QUE])
    print('Answer: ', art_dict[ANS], '\n')

    for p in art_dict[CTX]:
        print(p, '\n')
