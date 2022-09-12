#This script will create AMIs of all instances in the 'running state'
#The instance must have aws-cli installed and configured.
#The credentails used to login the cli should have ec2 and s3 full access
import boto3
import subprocess
import datetime
today = datetime.datetime.now()
date_time = today.strftime("%m/%d/%Y-%H.%M.%S")
print(date_time)
ec2 = boto3.resource('ec2', region_name='us-east-1')
image_ids = []
instances = ec2.instances.filter(
 Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
 print(instance.id,instance.placement)
 image = instance.create_image(Name=date_time+' AMI '+instance.id)
 print(image)
 image_ids.append(image.id)

for ami in image_ids:
 client = boto3.client('ec2')
 waiter = client.get_waiter('image_available')
 waiter.wait(Filters=[{
  'Name': 'image-id',
  'Values': [str(ami)]
 }])
 print('AMI has been created')
 bashCommand = "aws ec2 create-store-image-task \
   --image-id %s \
   --bucket ami-upload-test" %(ami)
 process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
 output, error = process.communicate()

