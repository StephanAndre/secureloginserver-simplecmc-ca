# secureloginserver-simplecmc-ca-demo
A simple CA with SIMPLE-CMC protocol support to test with a Secure Login Server.

This is just a demo. Do not use it for productive systems.

Free to use according to SAP Sample Code License Agreement v1.0.pdf.

## installation
Put all files to a new folder in a server that can be reached by your SLS (e.g. same system).

Then run
```
create-ca.sh
python simple-cmc-ca.py --port 8000 --post ON
```

In AS JAVA, create a new HTTP Destination with URL = http://sso.mo.sap.corp:8000/simple.csr.

Test with ping should work and make your python server print out a line.

Create a new SLS Remote CA of type "CMC - Simple" and select the new HTTP Destination.

Enable Remote CA should work.

## test
Use with your certificate lifecycle client:

```
rm sec/*
sapgenpse gen_pse -p ra.pse CN=SID
sapgenpse maintain_pk -p ra.pse -a SAP\ SE/SAP\ Global\ Root\ CA.cer 
sapgenpse gen_pse -p snc.pse CN=SNC
sapslscli enroll -r ra.pse -u psemaint -x $(pass psemaint) -e https://sso.mo.sap.corp:443/SecureLoginServer/slc3/doLogin?profile=simplera
sapslscli renew -r ra.pse -p snc.pse -e https://sso.mo.sap.corp:20443/SecureLoginServer/slc3/doLogin?profile=simplesnc
sapslscli renew -r ra.pse -p snc.pse -e https://sso.mo.sap.corp:20443/SecureLoginServer/slc3/doLogin?profile=simplesnc
