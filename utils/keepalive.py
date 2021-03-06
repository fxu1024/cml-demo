#This simple script re-tags aws instances expiration dates.  Run in a job.

!pip3 install boto3

import boto3
import datetime

#Set AWS creds here or in arguments for the project/engine.
#AWS_ACCESS_KEY_ID = '<ID>'
#AWS_SECRET_ACCESS_KEY = '<KEY>'
#regions = ['us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1','ap-southeast-1','ap-southeast-2','ap-northeast-1']
regions = ['us-west-2']
vpc = 'vpc-xxxxxxxxxx'

newdate=datetime.date.today() + datetime.timedelta(days=5)
newdate = newdate.strftime("%m%d%Y")

for region in regions: 
  
  ec2 = boto3.client("ec2", region_name=region)
  ec2res = boto3.resource("ec2", region_name=region)

  response = ec2.describe_instances(Filters=[
    {'Name':'vpc-id', 'Values':[vpc]}])
  for reservation in response["Reservations"]:
      for instance in reservation["Instances"]:
        for tags in instance["Tags"]:
          if tags["Key"] == 'enddate':
              print("InstanceID: " + instance["InstanceId"] + " Current Date: " + tags["Value"])
              
        ec2res.create_tags(Resources=[instance["InstanceId"]], 
                           Tags=[{'Key':'enddate', 'Value':newdate}])
  
  response = ec2.describe_instances(Filters=[
    {'Name':'vpc-id', 'Values':[vpc]}])
  for reservation in response["Reservations"]:
      for instance in reservation["Instances"]:
        for tags in instance["Tags"]:
          if tags["Key"] == 'enddate':
              print("InstanceID: " + instance["InstanceId"] + " New Date: " + tags["Value"])
