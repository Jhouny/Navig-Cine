FROM ontotext/graphdb:11.2.0

RUN mkdir -p /opt/graphdb/dist/conf \
    && mkdir -p /opt/graphdb/dist/data/repositories \
    && mkdir -p /opt/graphdb/dist/data/import

COPY data/conf/ /opt/graphdb/dist/conf/
COPY data/repositories/ /opt/graphdb/dist/data/repositories/
COPY data/import/ /opt/graphdb/dist/data/import/

# Copy the custom entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
