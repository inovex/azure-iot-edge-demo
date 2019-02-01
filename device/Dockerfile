FROM resin/raspberrypi3-debian:stretch

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends libboost-python1.62.0 python3-pip libpython3-dev && \
    rm -rf /var/lib/apt/lists/* 

RUN pip3 install --upgrade pip 
RUN pip install --upgrade setuptools 
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash moduleuser
USER moduleuser

ENTRYPOINT [ "python3", "-u", "./device.py", "simulate", "HostName=iotedgedemo.azure-devices.net;DeviceId=edge-device-1;SharedAccessKey=UXmF4s1XqQuWAuI/BwrD97cFy+7tu0n5pB+K+0BOzx0="]