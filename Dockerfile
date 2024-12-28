# Sử dụng Python 3.9 làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements.txt và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Expose port 5000
EXPOSE 5000

# Khởi chạy ứng dụng
CMD ["python", "app.py"] 