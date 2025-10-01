#!/bin/bash
docker-compose run --rm test pytest --cov=apps/users -v
