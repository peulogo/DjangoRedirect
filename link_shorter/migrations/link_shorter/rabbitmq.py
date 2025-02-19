import pika
import json
import logging

logger = logging.getLogger(__name__)


class RabbitMQ:
    def __init__(self, host="rabbitmq", username="rmuser", password="rmpassword"):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):

        try:
            credentials = pika.PlainCredentials(self.username, self.password)
            parameters = pika.ConnectionParameters(host=self.host, credentials=credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()

            self.channel.exchange_declare(exchange="statistic_service", exchange_type="direct", durable=True)

            logger.info("Connected to RabbitMQ successfully")

        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None

    def send_message(self, message: dict):

        if not self.channel:
            logger.error("RabbitMQ channel is not available")
            return

        try:
            self.channel.basic_publish(
                exchange="statistic_service",
                routing_key="click.log",
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            logger.info(f"Message sent to RabbitMQ: {message}")

        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to send message to RabbitMQ: {e}")

    def close_connection(self):

        if self.connection:
            self.connection.close()
            logger.info("RabbitMQ connection closed")


rabbitmq = RabbitMQ()
