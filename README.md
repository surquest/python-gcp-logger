![GitHub](https://img.shields.io/github/license/surquest/python-gcp-logger?style=flat-square)
![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/surquest/python-gcp-logger/test.yml?branch=main&style=flat-square)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/surquest/6e25c317000917840152a5e702e71963/raw/python-gcp-logger.json&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/surquest-GCP-logger?style=flat-square)

# Introduction

This project provides easy to use wrapper around the Google Cloud Platform logging library to simplify creation of the traced logs.

# Quick Start

```python
from surquest.GCP.logger import Logger

logger = Logger()
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

## FastAPI integration

Following example shows how to integrate the Tracer class with FastAPI endpoints:

```python
from surquest.GCP.logger import Logger
import requests
from fastapi import FastAPI, Depends, Query, Path

app = FastAPI()

@app.get("/exchange/currencies/{base}/{quote}")
async def exchange(
        base: str = Path(..., description="Base currency"),
        quote: str = Path(..., description="Quote currency"),
        amount: float = Query(..., gt=0, description="Amount to exchange"),
        logger: Logger = Depends(Logger)
):
    
    # get exchange rate from external API
    response = requests.get(
            f"https://api.exchangeratesapi.io/v1/latest?base={base}&symbols={quote}",
            params={
                "base": base,
                "symbols": quote,
                "access_key": "<your_api_key>" # please set your own API key
            }
        ).json()["rates"][quote]
    
    if 200 <= response.status_code < 300:
        
        exchange_rate = response.json()["rates"][quote]
        logger.info(
            msg="Retrieval of Exchange rates finished successfully",
            **{
                "currencies": {
                    "base": base,
                    "quote": quote
                },
                "exchangeRate": exchange_rate
            }
        )
        
    else:
        
        logger.error(
            msg="Failed to retrieve exchange rate",
            base=base,
            quote=quote,
            amount=amount,
            response=response
        )
        
        return {
            "info": "Failed to retrieve exchange rate",
            "error": response.text
        }
    
    result = amount * exchange_rate
        
    return {
        "currencies": {
            "base": base,
            "quote": quote
        },
        "amount": {
            "base": amount,
            "quote": result
        }
    }

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
