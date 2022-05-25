FROM python:alpine3.11
COPY . /lib
WORKDIR /lib 
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT ["python3"]
CMD ["./lib/app.py"]

