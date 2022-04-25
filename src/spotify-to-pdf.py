import sys
from spotify import get_playlist
from pdf import create_pdf
from mail import send_mail
from ftp import save_pdf

def main(args):
    pl_id = args[1]
    email = args[2]
    
    playlist = get_playlist(pl_id)
    pdf = create_pdf(playlist)
    name = playlist["name"]

    send_mail(email, name, pdf)
    save_pdf(pdf, name)

if __name__ == '__main__':
    main(sys.argv)
