FROM openjdk
COPY main.py /deployments/
COPY user_auth.py /deployments/
CMD cd /deployments; python main.py; python user_auth.py
