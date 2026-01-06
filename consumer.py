import pika, json, time, os, random
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transactions.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
HOST = os.getenv('BROKER_HOST', 'localhost')
USER = os.getenv('BROKER_USER', 'user')
PASS = os.getenv('BROKER_PASS', 'password')

# Setup Connection
credentials = pika.PlainCredentials(USER, PASS)
parameters = pika.ConnectionParameters(HOST, 5672, '/', credentials)

print("Connecting to RabbitMQ...")
while True:
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.AMQPConnectionError:
        print("Waiting for RabbitMQ...")
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue='demo_queue', durable=True)

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        order_id = message.get('order_id')
        amount = message.get('amount')
        timestamp = message.get('timestamp')
        
        # Convert timestamp to readable format
        readable_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # Log the transaction
        logger.info(
            f"Transaction processed - Order ID: {order_id}, "
            f"Amount: ${amount:.2f}, "
            f"Timestamp: {readable_time} ({timestamp})"
        )
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        logger.error(f"Error processing transaction: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

print("Consumer started. Waiting for messages...")
channel.basic_consume(queue='demo_queue', on_message_callback=callback)
channel.start_consuming()