FROM ubuntu
MAINTAINER dsa dsa@dsa.tech
RUN apt-get -y update
RUN apt-get -y install python-setuptools python-dev build-essential
COPY get-pip.py /
RUN python get-pip.py
RUN pip install flask
COPY server.py /
COPY generator.py /
COPY test_generator.py /
# EXPOSE 5000
# CMD python server.py
CMD python test_generator.py
