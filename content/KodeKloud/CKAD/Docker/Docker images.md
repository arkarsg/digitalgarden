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

---

# Commands vs Entrypoint

`docker run ubuntu` runs an instance of ubuntu image and exits immediately.

Unlike virtual machines, containers are not meant to host an OS. It is meant to run a specific tasks or process such as an application server. When the process is completed, the container exits.

## Defining the process

`CMD` instruction defines the program that runs within the container

**Append commands**

`docker run ubuntu sleep 5`

Appending commands overwrites the `CMD` instruction in the Docker image.

**Create your own image**
```dockerfile
FROM Ubuntu
CMD ["sleep", "5"]
```

The executable command and parameter needs to be different elements in an array.

### Entrypoint
Specifies the program when the container starts. Then command line args get appended
```Dockerfile
FROM Ubuntu
ENTRYPOINT ["sleep"]
```

Then,
```bash
docker run ubuntu-sleeper 10
```

will sleep for 10 seconds.

However, this will throw an error if there is no CLI argument. To define a default argument, 

```Dockerfile
FROM Ubuntu

ENTRYPOINT ["sleep"]
CMD ["5"]
```

This defaults 5 seconds to sleep.

To override the entrypoint, use `--entry-point`.


