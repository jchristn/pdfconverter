# PDF Converter Microservice

Microservice using LibreOffice to convert input documents to PDF.

## Feedback and Issues

Have feedback or issues?  Please file an issue here.

## Getting Started

Refer to the Docker-related files in the repo.  The Docker image is available on Docker Hub as `jchristn/pdfconverter` and can be downloaded [here](https://hub.docker.com/r/jchristn/pdfconverter).

This microservice exposes a RESTful endpoint on port `8000` and is called by sending the byte contents from an input file to the `POST /convert` endpoint.

```
POST /convert
... byte array from original file ...

Response: 200/OK
Content-Type: application/octet-stream
... byte array from PDF ...
```

You can call `GET` or `HEAD` to the root URL for a healthcheck.  These endpoints will always return a `200/OK`.

## Version History

Please refer to CHANGELOG.md
