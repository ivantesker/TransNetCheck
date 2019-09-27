FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04

RUN useradd -ms /bin/bash osa

RUN apt-get update                                                                                            && \
    apt-get install -y apt-utils curl software-properties-common build-essential

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update                                                                                            && \
    apt-get install -y libssl-dev libvips-dev libnss3-dev dbus-x11 nautilus libxss1 dbus-user-session python3    \
                       libgconf-2-4 wget netcat apt-transport-https libgl1-mesa-dev cheese nodejs python3-pip    \
		       libcanberra-gtk-module libcanberra-gtk3-module libudev-dev libusb-1.0-0-dev usbutils      \
		       cmake python3-dev sudo redis postgresql-client ffmpeg                                  && \
    npm install -g punycode har                                                                               && \
    npm install -g electron --unsafe-perm=true                                                               

RUN pip3 install coloredlogs opencv-python scipy pandas redis dlib joblib xgboost sklearn
RUN pip3 install https://download.pytorch.org/whl/cu100/torch-1.1.0-cp36-cp36m-linux_x86_64.whl \
                 https://download.pytorch.org/whl/cu100/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl
RUN pip3 install tensorflow-gpu

COPY OKO /home/osa/Desktop/OKO

WORKDIR /home/osa/Desktop/OKO
RUN chown osa /home/osa/Desktop/OKO -R
RUN npm install

CMD [ "./run.sh" ]
