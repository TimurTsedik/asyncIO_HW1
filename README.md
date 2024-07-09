### запускаем 
docker-compose up -d
### запускаем миграции
python3 migrate.py
### запускаем скачивание данных
python3 load_data.py
### проверяем данные
python3 check_data.py

