FROM ghcr.io/borncrusader/stanford-k8s-nextflow-demo-base:latest

RUN mkdir -p /home/demouser/models/angles

# Add files
ADD models/angles/predicting_angles.py /home/demouser/models/angles
ADD models/angles/resnet_1d_angles.py /home/demouser/models/angles

# Add common
EXPOSE 5000/tcp

ADD util/run_and_monitor.py /home/demouser

VOLUME /home/demouser/data

WORKDIR /home/demouser/models

ENTRYPOINT ["python3", "/home/demouser/run_and_monitor.py", "python3 angles/predicting_angles.py"]
