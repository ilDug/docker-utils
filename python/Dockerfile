FROM python:3.10
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD [ "python", "-u", "./main.py" ]

# la -u è per mostrare i print nel log (UNBUFFERED=1)