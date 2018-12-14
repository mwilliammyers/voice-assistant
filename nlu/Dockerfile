FROM japaric/arm-unknown-linux-musleabi

RUN dpkg --add-architecture armhf && \
    echo "deb http://ports.ubuntu.com/ubuntu-ports/ xenial main" >> /etc/apt/sources.list && \
    echo "deb-src http://ports.ubuntu.com/ubuntu-ports/ xenial main" >> /etc/apt/sources.list && \
    echo "deb http://ports.ubuntu.com/ubuntu-ports/ xenial-updates main" >> /etc/apt/sources.list && \
    echo "deb-src http://ports.ubuntu.com/ubuntu-ports/ xenial-updates main" >> /etc/apt/sources.list && \
    echo "deb http://ports.ubuntu.com/ubuntu-ports/ xenial-security main" >> /etc/apt/sources.list && \
    echo "deb-src http://ports.ubuntu.com/ubuntu-ports/ xenial-security main" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y build-essential:armhf llvm-3.9-dev:armhf libclang-3.9-dev:armhf clang-3.9:armhf

