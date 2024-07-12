# پروژه جنگویی با داکر

این پروژه یک برنامه جنگویی است که از داکر برای ساخت و اجرا استفاده می‌کند. در این فایل README نحوه‌ی راه‌اندازی و اجرای پروژه را توضیح می‌دهیم.

## پیش‌نیازها

قبل از شروع، اطمینان حاصل کنید که نرم‌افزارهای زیر روی سیستم شما نصب شده باشند:

- [Docker](https://www.docker.com/get-started)

## مراحل راه‌اندازی

### 1. کلون کردن مخزن

ابتدا مخزن پروژه را کلون کنید:

```bash
git clone <URL-مخزن-شما>
cd <نام-پوشه-مخزن>
```

### 2. ساخت ایمیج داکر

با استفاده از دستور زیر ایمیج داکر پروژه را بسازید:

```bash
docker build -t django_project .
```

### 3. اجرای کانتینر داکر

برای اجرای کانتینر داکر از دستور زیر استفاده کنید:

```bash
docker run -p 8000:8000 django_project
```

این دستور کانتینر را اجرا کرده و پورت 8000 روی میزبان را به پورت 8000 داخل کانتینر متصل می‌کند.

### 4. دسترسی به برنامه

پس از اجرای کانتینر، می‌توانید به برنامه جنگویی خود از طریق آدرس زیر دسترسی پیدا کنید:

```
http://localhost:8000
```

## فایل داکر

در زیر فایل داکر استفاده شده در این پروژه را مشاهده می‌کنید:

```dockerfile
# Use the official Ubuntu base image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev libpq-dev

# Create and set the working directory
RUN mkdir /code
WORKDIR /code

# Copy the requirements file into the image
COPY requirements.txt /code/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the image
COPY . /code/

# Expose the port that the app runs on
EXPOSE 8000

# Command to run tests
CMD ["python3", "manage.py", "test"]

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

این فایل مراحل زیر را انجام می‌دهد:

1. استفاده از تصویر رسمی اوبونتو به عنوان پایه
2. نصب وابستگی‌های لازم
3. ایجاد و تنظیم دایرکتوری کاری
4. کپی کردن فایل `requirements.txt` به تصویر
5. نصب وابستگی‌های پایتون
6. کپی کردن باقی کدهای برنامه به تصویر
7. باز کردن پورت 8000
8. اجرای دستورات برای تست و اجرای برنامه

## اجرای تست‌ها

برای اجرای تست‌ها می‌توانید دستور زیر را در کانتینر اجرا کنید:

```bash
docker run django_project python3 manage.py test
```

این دستور تست‌های جنگویی را اجرا می‌کند و نتایج را نمایش می‌دهد.

## نتیجه‌گیری

شما اکنون می‌توانید پروژه جنگویی خود را با استفاده از داکر راه‌اندازی و اجرا کنید. اگر سوالی داشتید یا به مشکلی برخوردید، لطفاً به مستندات داکر مراجعه کنید یا با ما تماس بگیرید.