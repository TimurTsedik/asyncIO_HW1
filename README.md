### Start the Containers
docker-compose up -d

### Run Migrations
python3 migrate.py

### Start Data Download
python3 load_data.py

### Verify Data
python3 check_data.py
