FROM python:3.9-slim

COPY . /prmexporter

RUN cd /prmexporter && python setup.py install

ENTRYPOINT ["python", "-m", "prmexporter.main"]
