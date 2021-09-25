import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'graph_editor'))

from parallelization import paint_lgraph_from_file
from graph_editor.screen import Screen
import argparse

parser = argparse.ArgumentParser(description='Grounded-L graph visualizer')

parser.add_argument(
    '-i', 
    '--input-file', 
    help='File with the input graph. ' 
    'Defauls to empty graph'
)
parser.add_argument(
    '-o', 
    '--output-file', 
    help='File to save the output of graph editor to. '
    'This has nothing to do with the grounded-l representation. ' 
    'Defaults to \'graph.txt\''
)

class Args:
    def __init__(self, input_file=None, output_file=None):
        self.input_file = input_file
        self.output_file = output_file

if __name__ == '__main__':
    args = parser.parse_args(namespace=Args)
    s = Screen(
        submit_fn=paint_lgraph_from_file,
        submit_button_text='Paint lgraph',
        submit_button_tooltip='Paint grounded lgraph representation of current graph',
        input_file=args.input_file,
        output_file=args.output_file,
    )
