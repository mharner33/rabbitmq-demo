# RabbitMQ Transaction Demo

A demonstration project showcasing RabbitMQ message queuing with a producer-consumer pattern for processing transaction messages. The project includes comprehensive logging and Datadog integration for monitoring and observability.

## Overview

This project simulates a transaction processing system where:
- **Producer**: Continuously generates and sends transaction messages to a RabbitMQ queue
- **Consumer**: Processes messages from the queue and logs each transaction
- **RabbitMQ**: Message broker that handles message queuing and delivery
- **Datadog Agent**: Collects metrics, traces, and logs for observability

Each transaction message contains:
- `order_id`: Random order identifier (1000-9999)
- `amount`: Random transaction amount ($10.00 - $500.00)
- `timestamp`: Unix timestamp of when the transaction was created

## Architecture
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Producer │ ───> │ RabbitMQ │ ───> │ Consumer │
└──────────┘ └──────────┘ └──────────┘
│
v
┌──────────┐
│ Datadog │
│ Agent │
└──────────┘


## Features

- **Durable Queues**: Messages are persisted to disk, ensuring no data loss
- **Transaction Logging**: All transactions are logged with order_id, amount, and timestamp
- **Error Handling**: Consumer includes error handling for malformed messages
- **Observability**: Integrated with Datadog for distributed tracing and monitoring
- **Auto-reconnection**: Both producer and consumer automatically reconnect if RabbitMQ is unavailable

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (if running locally)
- Datadog API key (optional, for Datadog integration)

## Quick Start

### Using Docker Compose (Recommended)

1. **Set up Datadog API key** (optional):
   export DD_API_KEY=your_datadog_api_key_here
   2. **Start all services**:
   
   docker-compose up
   3. **Access RabbitMQ Management UI**:
   - Open http://localhost:15672
   - Username: `demo`
   - Password: `demo1234`

4. **View transaction logs**:h
   # In another terminal
   tail -f transactions.log
   
### Running Locally (without Docker)

1. **Install dependencies**:
   pip install pika ddtrace
   2. **Start RabbitMQ** (using Docker):
   docker-compose up rabbitmq
   3. **Run the producer** (in one terminal):
   python producer.py
   4. **Run the consumer** (in another terminal):
   python consumer.py
   ## Configuration

### Environment Variables

#### Producer
- `BROKER_HOST`: RabbitMQ host (default: `localhost`)
- `BROKER_USER`: RabbitMQ username (default: `user`)
- `BROKER_PASS`: RabbitMQ password (default: `password`)
- `PUBLISH_INTERVAL`: Seconds between messages (default: `1.0`)

#### Consumer
- `BROKER_HOST`: RabbitMQ host (default: `localhost`)
- `BROKER_USER`: RabbitMQ username (default: `user`)
- `BROKER_PASS`: RabbitMQ password (default: `password`)

#### Docker Compose
The `docker-compose.yml` file configures:
- Producer sends messages every **0.5 seconds**
- RabbitMQ credentials: `demo` / `demo1234`
- Datadog integration (if `DD_API_KEY` is set)

## Logging

All transactions are logged to:
- **File**: `transactions.log` (in the project directory)
- **Console**: Standard output

Log format includes:
- Timestamp
- Order ID
- Amount (formatted as currency)
- Timestamp (both human-readable and Unix format)

Example log entry:
   docker-compose upRabbitMQ Management UI
- URL: http://localhost:15672
- View queues, connections, and message rates
- Monitor queue depth and consumer status

### Datadog (if configured)
- Distributed tracing across producer → RabbitMQ → consumer
- Service maps showing message flow
- Performance metrics and logs
- Set `DD_API_KEY` environment variable to enable

## Project Structure
rabbitmq/
├── producer.py          # Message producer script
├── consumer.py          # Message consumer script
├── docker-compose.yml   # Docker Compose configuration
├── pyproject.toml       # Python dependencies
├── transactions.log     # Transaction log file (generated at runtime)
└── README.md           # This file

Stopping the Services
Press Ctrl+C to stop the services, or run:
docker-compose down

To remove volumes (clears RabbitMQ data):
docker-compose down -v
