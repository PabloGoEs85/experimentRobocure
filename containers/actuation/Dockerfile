# Install ubuntu
FROM ubuntu:xenial

# Add package keyserver for ros
RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt-get update

# Install necessary packages
RUN apt-get -y install ros-kinetic-ros-base ros-kinetic-naoqi-driver ros-kinetic-pepper-robot ros-kinetic-pepper-meshes
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN apt-get -y install libzbar0 libzbar-dev
RUN apt-get -y install git

# install pip dependencies
RUN pip install zbarlight

# Initialize rosdep
RUN rosdep init

# Add user, ros doesn't work correctly with root
RUN useradd --create-home --shell=/bin/bash rosuser
USER rosuser

# Create directory for storing files 'naoqi'
RUN mkdir /home/rosuser/naoqi
WORKDIR /home/rosuser/naoqi

# Copy files from docker context & give permissions to 'rosuser'
COPY naoqi-sdk-2.5.5.5-linux64.tar.gz pynaoqi-python2.7-2.5.5.5-linux64.tar.gz ./
USER root
RUN chown rosuser:rosuser naoqi-sdk-2.5.5.5-linux64.tar.gz && chown rosuser:rosuser pynaoqi-python2.7-2.5.5.5-linux64.tar.gz
USER rosuser
RUN tar xzf ./naoqi-sdk-2.5.5.5-linux64.tar.gz
RUN tar xzf ./pynaoqi-python2.7-2.5.5.5-linux64.tar.gz

# Rosdep update run as 'rosuser'
RUN rosdep update

# Update python path
ENV PYTHONPATH "/home/rosuser/naoqi/pynaoqi-python2.7-2.5.5.5-linux64/lib:/home/rosuser/naoqi/pynaoqi-python2.7-2.5.5.5-linux64/lib/python2.7/site-packages:$PYTHONPATH"

# Extract project1 into folder a new folder 'source'
ADD source.tar ./source
USER root
RUN chown -R rosuser:rosuser ./source
RUN chmod -R 777 ./source
USER rosuser

# Add launch file
ADD launch.sh /home/rosuser/naoqi
USER root
RUN chmod -R 777 /home/rosuser/naoqi/launch.sh
USER rosuser

# Run launchfile in bash (remove expose?)
ENTRYPOINT ["/bin/bash", "-c"]
CMD ["/home/rosuser/naoqi/launch.sh"]
