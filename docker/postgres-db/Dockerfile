FROM postgres:13.0
USER postgres
COPY ./postgres-db/docker-entrypoint-initdb.d /docker-entrypoint-initdb.d/
ENTRYPOINT ["docker-entrypoint.sh"]
EXPOSE 5432
CMD ["postgres"]
