# Repo for language model deployment
Repo for deploying language detection on fastapi wrapped in a docker, build on cloud run

# Installation steps
## Deploy with cloud function
- Cloud function run with a fix main.py file 
- If changes are needed please edit from there

```bash
gcloud functions deploy handler --runtime python37 --trigger-http --memory 2048 --region asia-southeast1
```

## Deploy with cloud run
1) Clone the repo
```bash
git clone
```

2) Build image from gcloud
```bash
gcloud builds submit --tag asia.gcr.io/dialogflow-ex/lang-det
```

3) Build to cloud run and set limit to 2G for tensorflow
```bash
gcloud run deploy --image asia.gcr.io/dialogflow-ex/lang-det --memory 2G
```

4) Test build
```bash
gcloud auth print-identity-token > test/identity.txt # Store token locally
cd test/
python http_test.py
```
