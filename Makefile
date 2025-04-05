.PHONY: docker-compose-up-langfuse
docker-compose-up-langfuse:
	docker compose -f langfuse/compose.yaml up -d

.PHONY: docker-compose-down-langfuse
docker-compose-down-langfuse:
	docker compose -f langfuse/compose.yaml down
