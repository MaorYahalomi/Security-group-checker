FROM python:3.9-slim
COPY . /sg_rule_log
RUN pip install -r /sg_rule_log/requirements.txt
WORKDIR /sg_rule_log
CMD ["python", "main.py"]
