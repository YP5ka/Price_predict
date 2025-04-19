FROM bitnami/spark:latest

COPY spark-job.py /opt/spark-job.py

CMD ["/opt/bitnami/spark/bin/spark-submit", "/opt/spark-job.py"]
