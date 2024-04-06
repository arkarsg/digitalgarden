Creating your own image

- Cannot find a component or containerize for the ease of shipping

## Docker layers
1. OS - Ubuntu
2. Update apt repo
3. Install dependencies using `apt`
4. Install Python dependencies using `pip`
5. Copy source code to `/opt` folder
6. Run web server using `flask` command

```Dockerfile
FROM Ubuntu // defines base OS or another image

RUN apt-get update
RUN apt-get install python

RUN pip install flask
RUN pip install flask-mysql

COPY . /opt/source-code

ENTRYPOINT FLASK_APP=/opt/source-code/app.py flask run
```

The Docker file is in an `instruction` `arugment` format.

>[!important] 
>All Dockerfile must start with a `FROM` instruction

- `ENTRYPOINT` specifies the command that runs when the image is run
