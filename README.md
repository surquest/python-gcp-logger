# Introduction

This project provides easy to use wrapper around the Google Cloud Platform logging library to simplify creation of the traced logs.

# Quick Start

```python
from surquest.GCP.logger import Logger

# request is an object which allows to check the request headers
# request.headers.get('X-Cloud-Trace-Context', None)
request = None
logger = Logger(request=request)
logger.log(
    severity="INFO",
    msg="This is a test message",           # log message
    **{                                     # context information as KWARGS
        "key1": "value1",
        "key2": "value2"
    }
)

# Alternatively you can set the severity via the method name

logger.debug(msg="This is a DEBUG message")
logger.info(msg="This is a INFO message")
logger.warning(msg="This is a WARNING message")
logger.error(msg="This is a ERROR message")
logger.critical(msg="This is a CRITICAL message")
```

# Local development

You are more than welcome to contribute to this project. To make your start easier we have prepared a docker image with all the necessary tools to run it as interpreter for Pycharm or to run tests.


## Build docker image
```
docker build `
     --tag surquest/gcp/logger `
     --file package.base.dockerfile `
     --target test .
```

## Run tests
```
docker run --rm -it `
 -v "${pwd}:/opt/project" `
 -e "GOOGLE_APPLICATION_CREDENTIALS=/opt/project/credentials/keyfile.json" `
 -w "/opt/project/test" `
 surquest/gcp/logger pytest
```
