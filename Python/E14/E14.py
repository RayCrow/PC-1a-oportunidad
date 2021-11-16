import smtplib
import getpass
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
account = str(input('Ingresa el correo(GMAIL) con el cual lo quieres enviar: '))
password = getpass.getpass()
smtp.login(account,password)
print('Conexion con GMAIL exitosa')

to = str(input('Ingresa el correo destinatario: '))
subject = str(input('Con asunto: '))
body = str(input('Y cuerpo: '))

msg = MIMEMultipart()
msg['From'] = account
msg['To'] = to
msg['Subject']= subject
msg.attach(MIMEText(body))

file = open('Meme.jpg', "rb")
attach_image = MIMEImage(file.read(),_subtype='jpeg')
attach_image.add_header('Content-Disposition', 'attachment; filename = "Meme"')
msg.attach(attach_image)

smtp.sendmail(account,to,msg.as_string())

smtp.quit()