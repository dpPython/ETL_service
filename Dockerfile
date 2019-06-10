FROM python

ADD . /Contracts/service_api

WORKDIR /Contracts/service_api

COPY requirements.txt ./

RUN apt update && pip install --no-cache-dir -r requirements.txt

CMD ["python", "manage.py"]
