FROM python:3.13-slim AS build
WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip wheel --no-cache-dir --wheel-dir /wheels .

FROM python:3.13-slim
RUN useradd --system --uid 10001 --create-home migrationforge
WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels
COPY examples ./examples
RUN mkdir /data && chown migrationforge:migrationforge /data
USER 10001:10001
EXPOSE 8080
ENV MIGRATIONFORGE_DB=/data/migrationforge.db
ENTRYPOINT ["migrationforge-api"]
CMD ["examples/vmware-to-azure/250-vm-estate.json", "--port", "8080"]
