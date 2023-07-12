FROM python:3.11-slim

WORKDIR /iposter

#Installing required packages
COPY ./packages.txt ./packages.txt
RUN apt-get update
RUN apt-get -qq -y install curl
RUN xargs apt-get -qq -y install < packages.txt

#Creating virtual python env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

#Install packages to venv
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

CMD ["python3" "src/main.py"]