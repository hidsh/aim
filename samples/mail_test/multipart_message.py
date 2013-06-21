# email message /w gazo

# load image
fname = 'jobs.jpeg'
img = open(fname, 'rb').read()

# prepare message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

msg = MIMEMultipart()
msg_text = MIMEText('hello!')
msg_image = MIMEImage(img, 'jpeg', filename=fname)
msg_image.add_header("Content-Disposition", "attachment", filename=fname)

msg.attach(msg_text)
msg.attach(msg_image)

print msg
