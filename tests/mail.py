import smtplib
from email.header import Header
from email.mime.text import MIMEText

smtpObj = smtplib.SMTP("smtp.timeweb.ru", 25)
print("Connected")
msg = MIMEText("Спасибо", "plain", "utf-8")
msg["Subject"] = Header("Новая бронь", "utf-8")
msg["From"] = "support@voskresensky-hotel.ru"
msg["To"] = "support@voskresensky-hotel.ru"
smtpObj.starttls()
smtpObj.login("support@voskresensky-hotel.ru", "xxXX1234")
smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
smtpObj.quit()
