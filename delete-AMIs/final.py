import boto3
from dateutil.parser import parse
import datetime
import smtplib
age = 30
aws_profile_name = 'default'

def days_old(date):
    get_date_obj = parse(date)
    date_obj = get_date_obj.replace(tzinfo=None)
    diff = datetime.datetime.utcnow() - date_obj
    # print(diff.seconds//60)
    return diff.days
    # return diff.seconds//60

boto3.setup_default_session(profile_name = aws_profile_name)
ec2 = boto3.client('ec2')
output = "\n"
count = 0
amis = ec2.describe_images(Owners=[
        'self'
    ])
# print(amis)
for ami in amis['Images']:
    ifDelete = False
    create_date = ami['CreationDate']
    tagss = []
    if 'Tags' in ami:
        tagss = ami['Tags']
    ami_id = ami['ImageId']
    # print ami['ImageId'], ami['CreationDate']
    day_old = days_old(create_date)
    for tags in tagss:
        if tags["Key"] == 'delete' and tags["Value"] == 'yes':
            ifDelete = True

    # print(ifDelete)
    if day_old >= age and ami['Description']=='I can be deleted' and ifDelete==True:
    # if ami['Description']=='maybe I can be deleted':
        print "deleting -> " + ami_id + " - create_date = " + create_date
        count+=1
        output += "deleting -> " + ami_id + " - create_date = " + create_date + "\n"
        try:
           ec2.deregister_image(ImageId=ami_id)
           print "AMI deleted Successfully"
           output += "AMI deleted Successfully" + '\n'
        except smtplib.SMTPException as e:
           print "Error: unable to delete AMI"
           print(e)
           output+= "Error: unable to delete AMI"
           output+= e + "\n"

gmail_user = 'rajesh.tilwani3@gmail.com'
gmail_pwd = 'yourpassword'
sender = 'rajesh.tilwani3@gmail.com'
receivers = ['rajesh.tilwani3@gmail.com']

message = """From: From Rajesh <rajesh.tilwani3@gmail.com>
To: To Rajesh <rajesh.tilwani3@gmail.com>
Subject: AMIs Older than 30days deleted

No of AMIs to be deleted - """ + str(count) + "\n" + output



try:
   smtpObj = smtplib.SMTP('smtp.gmail.com',587)
   smtpObj.ehlo()
   smtpObj.starttls()
   smtpObj.ehlo
   smtpObj.login(gmail_user, gmail_pwd)
   smtpObj.sendmail(sender, receivers, message)
   print "Successfully sent email"
except smtplib.SMTPException as e:
   print "Error: unable to send email"
   print(e)
