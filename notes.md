# Introduction

This files contains notes of the Data Streaming Nanodegree from Udacity.

# Stream Processing

Stream is a potential unbounded sequence of data. Stream Processing consists in constantly making calculations and transformations in the data stream.

- Immutable data: data streams uses data that does not change once it is processed or when it is read.
- Usually small: data in a stream is commonly small up to 1Mb and may have a throughput of many thousands/s.
- Event: is an immutable fact recording something that happened in a system.
- Message Queues: communication commands between actions

### Batch vs Stream

Batch is a periodic analysis, usually scheduled, long processing time and may analyze historical data.

Stream processing runs when a event is generated, quick, limited time period and immutable data.

### Components of a Stream Processing Framework

- Streaming data store: stores the data in the order it arrived. Holds the immutable events and guarantee that it store and sends the data in order and that is was not changed.

### Logs in Data Streams

- Append only logs: logs of events are only appended in the end of a file, streams works like that.
- SQL database does the same thing with each event in the db (CDC).
- CDC or wall is only used for replication, not to be stored as useful data.
- Cassandra and HBase are examples of log-structure append only storage SQL-like. While Kafka is a message queue system.

# Kafka

Kafka is a stream processing tool and one of the most popular in the industry. It has the following properties:

- Store events
- Distributed
- Highly scalable
- Fault-tolerant

### Kafka Components

- Producers: sends events data to Kafka.
- Consumers: pull events data from Kafka topics.

### Kafka Clustering

- Kafka brokers are organized into clusters and needs a manager such as Zookeeper.

### Kafka Data

Data is stored in directories for each topic in each broker disk in a log format.

Also, the data is partitioned. The partitions are ordered and each partition has a leader broker. The partition can be replicated by a replication factor configured in other brokers.

- Partitions benefits: increases the speed that consumers can pull data by parallelization. Also produced data can be inserted partitioned.
- Replication: helps prevent data loss and unavailability (N-1 tolerance, where N is the replication factor).

### Kafka Topics

Important configuration options:

- replication per topic
- in Sync Replica (ISR)
- Number of ISR

Partitioning:

- Topics are divided into partitions
- Order is guarantee only within the partition
- The partitioning of a topic can be changed

``` 
Partitions = Max(Throughput/Producer Throughput, Throughput/Consumer Throughput)
```

##### Kafka Topic Name

- No official pattern, only < 256 chars
- Name using some strategy is recommended, such as a namespace with "." separator. Ex: ```<domain>.<name>.<event type>```

##### Topic Data Management

- Data expires after some time, size or both are reached
- It can be set to compacted, it is kept by oldest unique key
- Data can be compressed too.

### Kafka Producers

##### Sync vs Async Producer

- Synchronous Producer: waits a successful message delivery. Not very common.
- Asynchronous Producer: maximize throughput. Does not waits for a successful message, but still can receive a callback message. 
- Message Serialization: Kafka does not serializes the data, it should be handled by the app. One should not mix serialization types in the same topic.

##### Configuration

- set client.id
- Retries
- enable.idempotence to keep ordering with retries
- compression in individual topics
- Acks

##### Batch

Kafka clients sends data in batches, it can be configured by number of message, time and/or size.

### Kafka Consumers

##### Kafka Consumers

- Subscribe: if subscribing to an inexistent topic, the consumer will create it with default settings.
    - User can subscribe to a specific topic or a REGEX topic name.
- Offset: is the last message a consumer successfully consumed (consumer offset of a topic).
- Consumer Group: are collections of Kafka Consumers that consumes from the same topic, spreading the load to multiple consumers.
- Rebalance: if a consumer in a group is stopped/added/removed, Kafka assigns the partitions to the remaining consumers.
- Deserializers: deserialization of the data is responsibility of the consumer app 

### Kafka Performance

##### Consumer Performance

- Consumer lag: how far behind the consumer is `latest offset - consumer offset`
- Throughput: Messages/s
- Java Metrics Exporter or JMX: can be hooked to monitor and create performance dashboards.

##### Producer Performance

- Latency: high latency can be that acks are to high, too many partitions or too many replicas. latency = `time broker received - time produced`
- Producer response rate: messages delivered/time

##### Brokers Performance

- Disk usage: track disk free space
- Network usage: too many brokers can saturate network
- Election frequency: this should not be frequent. If too high indicates that a broker may be unstable.

### Removing Records and Privacy

Removing sensitive information from append only logs is a challenge. Message expiration is built within Kafka, allowing to delete data in a time frame or size.

Log compaction can be used to delete data from a specific key in a topic. This can be done by publishing NULL data to these keys. The problem is that the data is spread though many topics and does not expires by default.

##### Per-User Key Encryption

- A solution is to encrypt the user data. It is only possible to read the data with the key, thus by deleting the key, the data will be unreachable.


### Data Schemas and Apache Avro

Data schemas are important to maintain a data streaming pipeline working without error, specially for a consumer development independent of the producer.

##### Avro

Avro is a data serialization system that uses binary compression. It helps avoid deserialization errors and facilitates compression.

- Makes easier to update system with schema updates.
- Usually runs with schema registry.

##### Schema Evolution

Schema evolution is the process of changing schema with the system demands. Any changes in schemas can disrupt data consumers, that is why it is recommended to have a registry to be updated every time a schema is changed.

- Backward Compatibility: consumers are compatible from latest to older schemas version of data.
- Forward Compatibility: consumers using previous schema, can use the latest one.
- Full Compatibility: any schema is compatible with any version.
- No Compatibility: has no compatibility between schemas.

### Kafka Connect and REST Proxy

##### Connect

Framework that allows developers to configure a pre built code to integrate to common external sources such as SQL db, log files and HTTP.

##### The Kafka Connect API

In this exercise we're going to make use of the Kafka Connect API.

[See the documentation for more information on any of these actions](https://docs.confluent.io/current/connect/references/restapi.html).

###### Viewing Connectors

First, we can view connector-plugins:

`curl http://localhost:8083/connector-plugins | python -m json.tool`

Quick note, the `| python -m json.tool` above simply takes the output of the `curl` command and
prints the JSON nicely. You can omit this if you'd like!

##### Create a Connector

Lets create a connector. We'll dive into more details on how this works later.

```
curl -X POST -H 'Content-Type: application/json' -d '{
    "name": "first-connector",
    "config": {
        "connector.class": "FileStreamSource",
        "tasks.max": 1,
        "file": "/var/log/journal/confluent-kafka-connect.service.log",
        "topic": "kafka-connect-logs"
    }
  }' \
  http://localhost:8083/connectors
```

##### List connectors

We can list all configured connectors with:

`curl http://localhost:8083/connectors | python -m json.tool`

You can see our connector in the list.

##### Detailing connectors

Let's list details on our connector:

`curl http://localhost:8083/connectors/first-connector | python -m json.tool`

##### Pausing connectors

Sometimes its desirable to pause or restart connectors:

To pause:

`curl -X PUT http://localhost:8083/connectors/first-connector/pause`

To restart:

`curl -X POST http://localhost:8083/connectors/first-connector/restart`

##### Deleting connectors

Finally, to delete your connector:

`curl -X DELETE http://localhost:8083/connectors/first-connector`

##### REST Proxy

Kafka has a REST proxy to allow applications to communicate without the need of a client side producer or consumer.

### Stream Processing Fundamentals

Data streams are highly dynamic, making analytics on streams harder. A company may want to combine data streams to perform an action, but it is not guaranteed that different data streams will deliver data in the same pace, requiring some strategies:

- Combining: take more than one data stream to create another stream (ex: weather and stock market prices to predict my stock price)
- Filtering: filter a stream to make a stream more specific and refined for a given public.
- Remapping: change the form of data to remove fields or conform format (ex: take JSON data and transform into Avro).
- Aggregating: aggregate events to perform analysis or trigger events over a period of time.
- Windowing: period of time that the data stream will be analyzed.
    - Tumbling Window: fixed period of time repeating window without gap and overlap.
    - Hopping Window: window with duration and increment. It is possible to have gaps or overlapping.
    - Sliding Window: similar to hopping windows that increments in real time without gap.

# Streaming API Development and Documentation

