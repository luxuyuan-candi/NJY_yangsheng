FROM python:3.10-slim
WORKDIR /app

RUN apt update && \
apt install -y git && \
git clone https://github.com/luxuyuan-candi/NJY_yangsheng.git

WORKDIR /app/NJY_yangsheng

RUN python3 -m pip install --no-cache-dir -r backend/yaoshanbao/requirements.txt

CMD ["python3", "backend/yaoshanbao/server.py"]
