from screen import Screen
import argparse

parser = argparse.ArgumentParser(description='Graph editor')

parser.add_argument(
    '-i', 
    '--input-file', 
    help='File with the input graph. Defauls to empty graph'
)
parser.add_argument(
    '-o', 
    '--output-file', 
    help='File to save the output graph to. Defaults to \'graph.txt\''
)

class Args:
    def __init__(self, input_file=None, output_file=None):
        self.input_file = input_file
        self.output_file = output_file

if __name__ == '__main__':
    args = parser.parse_args(namespace=Args)
    s = None
    s = Screen(input_file=args.input_file, output_file=args.output_file)
