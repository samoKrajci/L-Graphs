from screen import Screen
import sys

if __name__ == '__main__':
    s = None
    if len(sys.argv) > 1:
        s = Screen(output_file=sys.argv[1])
    else:
        s = Screen()