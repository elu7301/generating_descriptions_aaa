IMAGE_NAME = description_generation
CONTAINER_NAME = description_generation_container

all: build run

build:
	docker build -t $(IMAGE_NAME) .

run: stop
	docker run -d -p 5000:5000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true

clean:
	-docker rmi $(IMAGE_NAME) || true

prune:
	docker system prune -f

logs:
	docker logs -f $(CONTAINER_NAME)

rebuild: clean build run

clean-all: stop clean prune

.PHONY: all build run stop clean prune logs rebuild clean-all
