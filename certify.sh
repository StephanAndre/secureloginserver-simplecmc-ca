#!/bin/sh

openssl req -in simple.csr -inform DER -text
echo "-----BEGIN CERTIFICATE REQUEST-----" > simple.csr.pem
base64 simple.csr >> simple.csr.pem
echo "-----END CERTIFICATE REQUEST-----" >> simple.csr.pem
openssl x509 -req -in simple.csr.pem -CA ca-root.pem -passin pass:1234 -CAkey ca-key.pem -CAcreateserial -outform PEM -out simple.pem -days 365
openssl crl2pkcs7 -nocrl -certfile simple.pem -out simple.p7b -certfile ca-root.pem
