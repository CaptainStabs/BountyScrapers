import smtplib

server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server_ssl.set_debuglevel(1)
server_ssl.ehlo()
