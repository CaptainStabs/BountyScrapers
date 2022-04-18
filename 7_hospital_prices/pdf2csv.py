import tabula
import argparse

def pdf2csv(args):
    tabula.convert_into(args.input, args.output, output_format="csv", pages=args.pages)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str)
    parser.add_argument('output', type=str)
    parser.add_argument('--pages', type=str, default='all')
    pdf2csv(parser.parse_args())
