#!/usr/bin/env python
#
# Author: Thamme Gowda [tg (at) isi (dot) edu] 
# Created: 4/12/20
import torch
import logging as log
import argparse
import sys

DEF_MODEL = 'pytorch/fairseq:xlmr.base'  # can also be xlmr.large or xmlr.base
log.basicConfig(level=log.INFO)

class LangModel:

    def __init__(self, name=DEF_MODEL):
        group, model_name = name.split(':')
        log.info(f"loading {group}  {model_name}")
        self.model = torch.hub.load(group, model_name)
        self.model.eval()
        if torch.cuda.is_available():
            log.info("Cuda is available and I'm going to use it."
                     "To disable, simply unset CUDA_VISIBLE_DEVICES variable")
            self.model = self.model.cuda()
        # TODO: move to GPU

    def force_decode(self, sentence):
        indices = self.model.encode(sentence).view(1, -1)  # [B=1 x T]
        feats = self.model.extract_features(indices)  # [B=1 x T x D]
        scores = self.model.model.output_layer(feats)  # [B=1 x T x V]
        log_probs = torch.log_softmax(scores, dim=-1)  # [B=1 x T x V]
        lop_probs = log_probs.gather(dim=2, index=indices.unsqueeze(2))  # [B x T x 1]
        log_prob = lop_probs.squeeze(2).sum(dim=1)  # [B=1 x T] -> [B=1]
        return torch.exp(log_prob).item()

def parse_args():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('-i', '--inp', type=argparse.FileType('r'), default=sys.stdin,
                   help='Input file path')
    p.add_argument('-o', '--out', type=argparse.FileType('w'), default=sys.stdout,
                   help='Output file path')
    p.add_argument('-n', '--name', default=DEF_MODEL,
                   help='Name of model -- a reference to pytorch hub')
    return p.parse_args()

def main():
    args = parse_args()
    lm = LangModel(name = args.name)
    log.info(f"reading from {args.inp}")
    for line in args.inp:
        sentence = line.replace('\t', ' ').strip()
        if sentence:
            score = lm.force_decode(sentence)
            args.out.write(f'{score:g}\t{sentence}\n')
        else:
            args.out.write(f'\t\n')


if __name__ == '__main__':
    main()