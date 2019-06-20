# Dockerfile for LAC

FROM paddle:dev

RUN git clone https://github.com/PaddlePaddle/Paddle.git ~/Paddle && cd ~/Paddle && git checkout v0.14.0 && \
    cd ~/Paddle && rm -rf cbuild && mkdir cbuild && cd cbuild && \
    cmake -DCMAKE_BUILD_TYPE=Release -DWITH_MKLDNN=OFF -DWITH_GPU=OFF -DWITH_FLUID_ONLY=ON .. && \
    make -j 8

RUN cd ~/Paddle && pip install cbuild/python/dist/paddlepaddle*.whl && \
    cd ~/Paddle/cbuild && make -j 8 inference_lib_dist

RUN cd /tmp && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh > /tmp/script.deb.sh && \
    bash script.deb.sh && \
    apt-get install git-lfs && \
    rm /tmp/script.deb.sh


RUN git clone https://github.com/cnglen/lac.git ~/lac && \
    cd ~/lac && git checkout for_paddle_v1.1 && mkdir build && cd build && cmake -DPADDLE_ROOT=/root/Paddle/cbuild/fluid_install_dir .. && \
    make && make install && \
    chmod u+x ~/lac/python/infer_fifo.py

ENTRYPOINT ["/root/lac/python/infer_fifo.py"]
CMD []

# How to build?
# docker build --tag=paddle:lac .

# How top run? YOUR_DATA_DIRECTORY/your_input_data.txt
# docker run -it -v YOUR_DATA_DIRECTORY:/lac_space paddle:lac -if /lac_space/your_input_data.txt
