# -*- coding: utf-8 -*-
"""
Created on Sun Jan  29 19:54:55 2023

@author: Jun Wu
"""
import argparse
from train import train
from predict import predict

def run_train(args):
    train(in_fasta=args.input_file, batch_size=args.batch_size, maxlen=200, min_seq=args.min_seq,
          arg_model = args.arg_model, cat_model = args.cat_model, cat_index= args.cat_index)

def run_predict(args):
    predict(in_fasta=args.input_file, batch_size= args.batch_size, maxlen=200, min_prob=args.min_prob,
            arg_model = args.arg_model, cat_model = args.cat_model, cat_index= args.cat_index,
            output_file = args.output_file)

def main():
    parser = argparse.ArgumentParser(prog='HiARG')
    subparsers = parser.add_subparsers()
    # run the prediction section
    hiarg_p = subparsers.add_parser("predict", help="Predict ARG from genes or ORF")
    hiarg_p.add_argument('-i', '--input-file', required=True, help='Input file (Fasta input file)')
    hiarg_p.add_argument('--arg-model', default='models/arg_model.pkl', help='Model for ARG identification')
    hiarg_p.add_argument('--cat-model', default='models/cat_model.pkl', help='Model for resistance category classification')
    hiarg_p.add_argument('--cat-index', default='models/Category_Index.csv', help='File for the resistance category index')
    hiarg_p.add_argument('-o', '--output-file', required=True, help='Output file where to store results')
    hiarg_p.add_argument('--min-prob', default=0.5, type=float, help='Minimum probability cutoff [Default: 0.5]')
    hiarg_p.add_argument('-b','--batch-size', default=10, type=float,help='Number of the samples fed to the model iteratively [Default: 10]')
    hiarg_p.set_defaults(func=run_predict)

    # run the train section
    hiarg_t = subparsers.add_parser("train", help="Retrain the HiARG models")
    hiarg_t.add_argument('-i', '--input-file', required=True, help='Input file (Fasta input file)')
    hiarg_t.add_argument('--arg-model', default='models/arg_model.pkl', help='Model for ARG identification')
    hiarg_t.add_argument('--cat-model', default='models/cat_model.pkl',
                         help='Model for resistance category classification')
    hiarg_t.add_argument('--cat-index', default='models/Category_Index.csv',
                         help='File for the resistance category index')
    hiarg_t.add_argument('--min-seq', default=50, type=float, help='Minimal sequence number for the category training [Default: 50]')
    hiarg_t.add_argument('-b', '--batch-size', default=10, type=float,
                         help='Number of the samples fed to the model iteratively [Default: 10]')
    hiarg_t.set_defaults(func=run_train)

    # Get all arguments
    args = parser.parse_args()
    args.func(args)
    pass

if __name__ == '__main__':
    main()
