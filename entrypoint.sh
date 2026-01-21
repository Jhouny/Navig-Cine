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

# Stop GraphDB process after repository creation
echo "Stopping GraphDB to import RDF data..."
kill $GRAPHDB_PID
wait $GRAPHDB_PID

# Import RDF data into the repository
echo "Importing RDF data into repository..."
/opt/graphdb/dist/bin/importrdf load -f -i Gdb-Navig-Cine -m parallel /opt/graphdb/dist/data/import/*.ttl

# Restart GraphDB to keep the container running
echo "Restarting GraphDB..."
/opt/graphdb/dist/bin/graphdb
