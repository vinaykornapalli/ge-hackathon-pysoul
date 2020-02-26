FROM python:3.6.10-slim

# RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
# RUN apt-get install -y python3-pip python3-dev 
 

LABEL Author="Vinay Kornapalli"
ENV FLASK_APP="pysoul/api/server.py"
ENV FLASK_ENV="development"

WORKDIR /pysoul-docker

COPY requirements.txt /pysoul-docker/requirements.txt
RUN pip install -r /pysoul-docker/requirements.txt

COPY /pysoul /pysoul-docker/pysoul
# COPY /packs /pysoul-docker/
COPY model.h5 /pysoul-docker/

COPY setup.py /pysoul-docker/

COPY /input /pysoul-docker/input

# RUN pip install --upgrade pip
# RUN pip3 install --upgrade pip
# RUN pip3 install virtualenv
# RUN virtualenv packs
# RUN /bin/bash -c "source /pysoul-docker/packs/bin/activate"

RUN pip install --editable /pysoul-docker/
EXPOSE 80
CMD ["python","./pysoul/api/server.py"]
