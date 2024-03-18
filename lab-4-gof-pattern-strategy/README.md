docker-compose up -d

docker ps

docker logs <kafka-container-id>

docker container exec -it <kafka-container-id> /bin/bash

kafka-console-producer --broker-list localhost:9092 --topic lab4-messages-topic

# to start a command line consumer
kafka-console-consumer --bootstrap-server localhost:9092 --topic lab4-messages-topic --from-beginning

docker-compose down
