import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'graph_editor'))

from parallelization import paint_lgraph_from_file
from graph_editor.screen import Screen

if __name__ == '__main__':
    s = Screen(
        submit_fn=paint_lgraph_from_file,
        submit_button_text='Paint lgraph',
        submit_button_tooltip='Paint grounded lgraph representation of current graph'
    )
