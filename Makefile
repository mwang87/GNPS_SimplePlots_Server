server-compose-build:
	docker-compose build

server-compose-interactive:
	docker-compose up --build

server-compose-server:
	docker-compose up --build -d

server-compose-production:
	docker-compose -f docker-compose.yml -f docker-compose-production.yml up -d

build:
	docker build -t gnps_plot .

build-no-cache:
	docker build --no-cache -t gnps_plot .
