chmod 777 ingested_data
chmod 777 error_on_ingestion
chmod 777  entrypoint.sh
chmod -R 777 data

docker-compose down
docker-compose up
