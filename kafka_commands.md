- List topics: ```kafka-topics --list --zookeeper localhost:2181```

- Create topics: ```kafka-topics --create --topic "my-first-topic" --partitions 1 --replication-factor 1 --zookeeper localhost:2181```

- Delete Topic: ```kafka-topics --delete --topic "my-first-topic" --zookeeper localhost:2181```

- Produce Data to a Topic : ```kafka-console-producer --topic "my-first-topic" --broker-list PLAINTEXT://localhost:9092```

- Consume data from beginning of Topic: ```kafka-console-consumer --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092 --from-beginning```

- Alter Topic Partitions: ```kafka-topics --alter --topic kafka-arch --partitions 3 --zookeeper localhost:2181```


```kafka-console-consumer --bootstrap-server localhost:9092 --topic "com.udacity.streams.clickevents.scored"```