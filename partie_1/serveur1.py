import boto3
import statistics
import time


# Get the service resource
sqs1 = boto3.resource('sqs')


#Get the queue
queueRequest = sqs1.get_queue_by_name(QueueName="requestQueue")

queue = sqs1.create_queue(QueueName='responseQueue', Attributes={
                'DelaySeconds': '0',

                })

while(1):


    try:
        for message in queueRequest.receive_messages():

            t=[int(n) for n in (format(message.body)).split()]
            print(t)
            minimum = min(t)
            maximum = max(t)
            sum1 = sum(t)
            length = len(t)
            average = sum1/length
            median = statistics.median(t)
            message1 = "minimum is %d " %(minimum) + " maximum is %d " %(maximum) +  " average is %d  " %(average) + " median is %d " %(median)
            print(message1)
            response = queue.send_message(MessageBody=message1)

            message.delete(QueueUrl='https://sqs.us-east-1.amazonaws.com/580530755374/requestQueue', ReceiptHandle=message.receipt_handle)
            print("request queue deleted")



    except:
        print("Exception")
