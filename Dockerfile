# Sử dụng một hình ảnh cơ sở Python
FROM python:3.11

# Sao chép tất cả các tệp từ thư mục hiện tại vào thư mục /app trong container
COPY . /app

# Đặt thư mục làm thư mục làm việc hiện tại
WORKDIR /app

# Cài đặt các phụ thuộc từ tệp requirements.txt
RUN pip install -r requirements.txt

# Expose cổng 8000 để truy cập ứng dụng Django
EXPOSE 8000

# Chạy lệnh để khởi chạy ứng dụng Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
