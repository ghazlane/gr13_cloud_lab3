import boto3
import time


s3=boto3.client('s3')
s3.upload_file('lab3-image.jpg','group13-lab3.part2','s3_image.jpg')

sqs1= boto3.resource('sqs')
# Create the queue. This returns an SQS.Queue instance
inboxQueue = sqs1.create_queue(QueueName='inboxQueue', Attributes={
                'DelaySeconds': '0'
                })



response = inboxQueue.send_message(MessageBody='s3_image.jpg')

time.sleep(6)


outboxQueue = sqs1.get_queue_by_name(QueueName="outboxQueue")

for message in outboxQueue.receive_messages():
    key=format(message.body)
    print(key)

    s3 = boto3.client('s3')
    s3.download_file('group13-lab3.part2', key ,'C:\\Users\\USER\\Desktop\\aws\\'+key)

    message.delete(QueueUrl='https://sqs.us-east-1.amazonaws.com/580530755374/outboxQueue', ReceiptHandle=message.receipt_handle)
    print("request queue deleted")