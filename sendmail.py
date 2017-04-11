# Import smtplib for the actual sending function
import smtplib, mimetypes

# Import the email modules we'll need
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

mail_relay_host  = "localhost"
fromAddr = 'no-reply@localdomain.com'

def sendmail(subject, html_description, attachments=None):

    toArr = ["email1", "email2"]
    toCc = []
    toBcc = []
    COMMASPACE = ', '


    # Creating a Multipart message
    mainMsg = MIMEMultipart()
    mainMsg['Subject'] = subject
    mainMsg['From'] = fromAddr
    mainMsg['To'] = COMMASPACE.join(toArr)
    mainMsg['Cc'] = COMMASPACE.join(toCc)

    #text = "Find the list of the Integration Failures."
    #msgBody = MIMEText(text, "plain")
    htmlBody = MIMEText(html_description, "html")
    mainMsg.attach(htmlBody)

    if attachments:
        for filename in attachments:
            attachment = MIMEBase('application', "octet-stream")
            attachment.set_payload(open('/tmp/' + filename, "rb").read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment; filename=' + filename)
            mainMsg.attach(attachment)
    

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    recipients = toArr 
    recipients.extend(toCc)
    recipients.extend(toBcc)
    s = smtplib.SMTP(mail_relay_host)
    s.sendmail(fromAddr, recipients, mainMsg.as_string())
    s.quit()
    
    
    html_description = ""
    attachments = []
    sendmail("Subject1", html_description, attachments)
    
