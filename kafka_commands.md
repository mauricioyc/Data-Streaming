- List topics: ```kafka-topics --list --zookeeper localhost:2181```

- Create topics: ```kafka-topics --create --topic "my-first-topic" --partitions 1 --replication-factor 1 --zookeeper localhost:2181```

- Delete Topic: ```kafka-topics --delete --topic "my-first-topic" --zookeeper localhost:2181```

- Produce Data to a Topic : ```kafka-console-producer --topic "my-first-topic" --broker-list PLAINTEXT://localhost:9092```

- Consume data from beginning of Topic: ```kafka-console-consumer --topic "my-first-topic" --bootstrap-server PLAINTEXT://localhost:9092 --from-beginning```

- Alter Topic Partitions: ```kafka-topics --alter --topic kafka-arch --partitions 3 --zookeeper localhost:2181```


docker-compose exec zookeeper kafka-topics --list --zookeeper localhost:2181
docker-compose exec zookeeper kafka-topics --zookeeper localhost:2181 --delete --topic 'weather_info'
docker-compose exec kafka0 kafka-console-consumer --topic "weather_info" --bootstrap-server PLAINTEXT://localhost:9092 --from-beginning

docker-compose exec kafka0 kafka-consumer-groups --bootstrap-server localhost:9092 --group "group_turnstile_summary" --describe
docker-compose exec kafka0 kafka-consumer-groups --bootstrap-server localhost:9092 --delete --group "group_turnstile_summary"


/data/kafka/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic withdrawals-location --from-beginning


/data/redis/redis-stable/src/redis-cli -a notreally

zrange Customer 0 -1

zadd Customer 0 "{\"customerName\":\"Sam Test 6\",\"email\":\"sam.test5@test.com\",\"phone\":\"18015551212\",\"birthDay\":\"2005-05-05\"}"

kafka-console-consumer --topic "redis-server" --bootstrap-server localhost:9092 --from-beginning

kafka-console-consumer --topic "balance-score" --bootstrap-server localhost:9092 --from-beginning

/data/spark/sbin/start-master.sh
/data/spark/sbin/start-slave.sh spark://73201679f328:7077