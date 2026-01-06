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
INTERVAL = float(os.getenv('PUBLISH_INTERVAL', '1.0'))

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

print("Producer started. Sending messages...")

while True:
    message = {
        'order_id': random.randint(1000, 9999),
        'amount': round(random.uniform(10.0, 500.0), 2),
        'timestamp': time.time()
    }
    
    channel.basic_publish(
        exchange='',
        routing_key='demo_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2) # Persistent
    )
    
    # Log the transaction
    readable_time = datetime.fromtimestamp(message['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    logger.info(
        f"Transaction sent - Order ID: {message['order_id']}, "
        f"Amount: ${message['amount']:.2f}, "
        f"Timestamp: {readable_time} ({message['timestamp']})"
    )
    
    print(f" [x] Sent Order {message['order_id']}")
    time.sleep(INTERVAL)