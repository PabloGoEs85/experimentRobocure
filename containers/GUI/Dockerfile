# Install ubuntu
FROM ubuntu:xenial

# Add package keyserver for ros
RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116
RUN echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list
RUN apt-get update

# Install necessary packages
RUN apt-get install -y ros-kinetic-ros-base
RUN apt-get -y install python-pip 
RUN pip install --upgrade pip
RUN apt-get -y install python-tk
RUN echo $DISPLAY

# Initialize rosdep
RUN rosdep init
RUN useradd --create-home --shell=/bin/bash rosuser
USER rosuser

# Create directory for storing files 'naoqi'
RUN mkdir /home/rosuser/naoqi
WORKDIR /home/rosuser/naoqi

# Rosdep update run as 'rosuser'
RUN rosdep update

# Extract project1 into folder a new folder 'source'
ADD source.tar ./source
USER root
RUN chown -R rosuser: ./source
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
