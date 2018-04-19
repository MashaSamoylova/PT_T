# PT_T

You need to create the docker container to run tests:
```
docker build -t sshdtest ./tests/
docker run -d -p 4000:22 -t sshdtest
```
To run tests:
```
pytest tests/testSSH.py
```
