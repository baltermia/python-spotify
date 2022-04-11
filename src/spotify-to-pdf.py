import sys
from venv import create
from spotify import get_playlist
from pdf import create_pdf
import codecs

def main(args):
    pl_id = args[1]

    playlist = get_playlist(pl_id)

    pdf = create_pdf(playlist)

    with open("out.pdf", "wb") as f:
        f.write(pdf)

if __name__ == '__main__':
    main(sys.argv)
