# Use the official MongoDB image as the base image
FROM mongo:latest

# Copy the initialization scripts to the docker-entrypoint-initdb.d directory
COPY insert_skins.js /docker-entrypoint-initdb.d/
COPY insert_users.js /docker-entrypoint-initdb.d/


# Set the scripts to be executable
RUN chmod +x /docker-entrypoint-initdb.d/insert_skins.js
RUN chmod +x /docker-entrypoint-initdb.d/insert_users.js
