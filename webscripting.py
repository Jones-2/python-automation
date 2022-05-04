from http import server
import requests #use for http request
from bs4 import BeautifulStoneSoup # use for web scraping
import smtplib #use for sending email

#Lines 6 and 7 are for the creation of the imail body
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import datetime

#email content holder
email_content=""

current_date= datetime.datetime.now()

#A function to extract the contents of the webpage
def extract_web_news(url="https://news.ycombinator.com/"):
    print("Trending Stories from Hacker News ...")
    cnt=" "
    cnt+=125*"*" #displays 125 star symbols
    response=requests.get(url) #extract the response from the given url
    content=response.content #extract the content from the returned  response
    soup=BeautifulStoneSoup(content, "html.parser")

    #loop through the content and extract the needed components of the site
    #k is the html tag
    for i, tag in range(soup.find_all('td', attrs={'class':'title','valign':' '})): cnt+=((str(i+1)+' :: '+tag.text, "\n", + "<br>") if tag.text!='More' else " ")
       

    return cnt

cnt=extract_web_news()
email_content=+cnt
email_content+=('<br></br> End of Message')

#Authenticating the email to send the content of the site to
print('Composing email ......')
#setting email parameters

SERVER='smtp.gmail.com'
PORT= 587
FROM= 'darijones6@gmail.com'
TO='darijones6@gmail.com'
PASS='password1'

#email body
msg= MIMEMultipart()
msg['Subject']="Trending Hacker News [Automated Email]" +' '+ str(current_date.day)+' '+str(current_date.month)+' ' +str(current_date.year)
msg['FROM']=FROM
msg['TO']=TO
msg.attach(MIMEText(email_content,'html'))

print("server is initializing ....")
server=smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM,TO, msg.as_string())
print("Email Sent Successfully")

server.quit()