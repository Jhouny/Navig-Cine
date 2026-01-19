#!/bin/bash

# Start GraphDB in the background
/opt/graphdb/dist/bin/graphdb &
GRAPHDB_PID=$!

# Wait for GraphDB to be ready
echo "Waiting for GraphDB to start..."
sleep 10

# Create repository using POST request
echo "Creating repository..."
curl -X POST -H "Content-Type: multipart/form-data" \
	-F "config=@/opt/graphdb/dist/data/repositories/Gdb-Navig-Cine.ttl" \
	http://localhost:7200/rest/repositories

# Wait for GraphDB process to keep container running
wait $GRAPHDB_PID
