from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
from sendgrid import SendGridAPIClient
from config import get_config
from base64 import b64encode

def send_mail(emails, name, pdf):
    config = get_config()["SENDGRID"]

    # create mail object
    message = Mail(
        from_email = "Spotify to PDF <{}>".format(config["email"]),
        to_emails = emails,
        subject = f"Export for playlist '{name}'",
        html_content = f"Hi!<br /><br />Your PDF for the playlist '{name}' is created and pinned for you to the attachments of this mail.<br />Hope you like it!<br /><br />Best Regards,<br />Spotify-to-PDF Team :)"
    )

    # add pdf as attachment
    message.attachment = Attachment(
            FileContent(b64encode(pdf).decode()),
            FileName(name + ".pdf"),
            FileType("application/pdf"),
            Disposition("attachment")
        )

    # send mail
    SendGridAPIClient(config["api_key"]).send(message)