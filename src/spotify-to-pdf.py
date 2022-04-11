import sys
from spotify import get_playlist

def main(args):
    pl_id = args[1]

    playlist = get_playlist(pl_id)

    print(playlist)

if __name__ == '__main__':
    main(sys.argv)
