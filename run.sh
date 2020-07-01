chmod 777 ingested_data
chmod 777 error_on_ingestion
chmod entrypoint.sh

docker-compose down
docker-compose up