FROM python:3.7
COPY requirement.txt .
RUN pip install -r requirement.txt
EXPOSE 80
COPY . /app
CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "80"]