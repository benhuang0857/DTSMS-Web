# 使用官方 Python 映像作為基礎映像
FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 進入容器
COPY requirements.txt /app

# 安裝虛擬環境和依賴
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案到容器
COPY . /app/

# 指定容器啟動時執行的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 開放端口
EXPOSE 8000
