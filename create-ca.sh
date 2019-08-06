#!/bin/sh

openssl genrsa -aes256 -passout pass:1234 -out ca-key.pem 2048
openssl req -x509 -new -nodes -extensions v3_ca -passin pass:1234 -key ca-key.pem -days 1024 -out ca-root.pem -sha512
