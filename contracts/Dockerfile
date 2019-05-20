FROM python


ADD . /Contracts/service_api

WORKDIR /Contracts/service_api

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python", "manage.py"]
