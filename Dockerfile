# start by pulling the python image
FROM ubuntu 
RUN apt update 
RUN apt install -y
RUN apt install apache2-utils -y
RUN apt install python3 python3-pip -y
RUN pip3 install flask
RUN apt clean

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt
COPY ./templates/ /app/templates/

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python3" ]

CMD ["pyraces.py" ]



