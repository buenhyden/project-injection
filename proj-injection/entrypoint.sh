#!/bin/sh

# PostgreSQL 데이터베이스가 준비될 때까지 대기
while ! nc -z release-proj-postgres 5432; do
  sleep 0.1
done

# Django Makemigrations
python manage.py makemigrations
# Django 마이그레이션 실행
python manage.py migrate

# 슈퍼유저 생성
# echo "from django.contrib.auth.models import Accounts; Accounts.objects.create_superuser('admin', '1qaz2wsx')" | python manage.py shell

# Django 서버 실행
exec "$@"