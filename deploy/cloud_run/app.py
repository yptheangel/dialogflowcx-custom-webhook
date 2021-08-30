from fastapi import FastAPI, Form, Request
import tensorflow as tf
import sys
import os
import logging
import json

#change this to your model's path
model_path = '../../models/lang_det_model'
if not os.path.exists(model_path):
    print('No model found exiting')
    sys.exit()

app = FastAPI()
model = tf.saved_model.load(model_path)
lang_labels = {
    0: "eng",
    1: "malay",
    2: "rojak",
    3: "manglish",
    4: "other"
}

@app.get('/')
async def index():
    print('Backend server is running')
    import sys
    sys.stdout.flush()
    return "Your model is Language Detection Model"

@app.get('/_ah/warmup')
async def warmup():
    # Handle your warmup logic here, e.g. set up a database connection pool
    return '', 200, {}

@app.post('/predict')
async def get_language(request: Request):
    body = await request.json()
    print(json.dumps(body))
    import sys
    sys.stdout.flush()
    
    preds = model([['This is an input string']])
    preds = tf.squeeze(preds, axis=0).numpy()

    return {
        'output_class': lang_labels[preds.argmax()],
        'class_prob': float(round(preds.max() * 100, 2))
    }