import boto3
from skimage import io
from skimage import exposure

sqs1 = boto3.resource('sqs')

#Get the inbox queue
inboxQueue = sqs1.get_queue_by_name(QueueName="inboxQueue")

# Create the queue. This returns an SQS.Queue instance
outboxQueue = sqs1.create_queue(QueueName='outboxQueue', Attributes={
                'DelaySeconds': '0'
                })

print(outboxQueue.url)

while(1):

	try:
		for message in inboxQueue.receive_messages():
			key=format(message.body)
			print(key)

			s3 = boto3.client('s3')
			s3.download_file('group13-lab3.part2', key ,'./'+key)


			loadedPic = io.imread('./'+key)
			image_equalized = exposure.equalize_hist(loadedPic)
			io.imsave('editedPic.png',image_equalized)

			s3=boto3.client('s3')
			s3.upload_file('editedPic.png','group13-lab3.part2','s3_Newimage.jpg')
			response = outboxQueue.send_message(MessageBody='s3_Newimage.jpg')

			message.delete(QueueUrl='https://sqs.us-east-1.amazonaws.com/580530755374/inboxQueue', ReceiptHandle=message.receipt_handle)
    except:
		print("Exception")