Для выполнения команд по shh, нужно добавить в папку с проектом файл с ключом - ssh_secret_key.pem

Метод для отлавливания вебхука - host:port/api/kuma/alert

В CLOUDFLARE_API_KEY нужно указывать global api key, иначе не будет прав для работы с зонами




----- через docker -----

устанавливаем docker: curl -sSL https://get.docker.com | sh

Копируем бота на сервер

Запускаем командой docker compose up --build

то же самое с обновлением. залили обнову - написали docker-compose up --build

