import numpy
import tensorflow as tf
from google.cloud import storage
import os

# We keep model as global variable so we don't have to reload it in case of warm invocations
model = None
load_model_at_local = True


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket and save the files to the serverless's RAM"""
    if not os.path.exists('/tmp/variables'):
        os.makedirs('/tmp/variables')
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print('Blob {} downloaded to {}.'.format(source_blob_name, destination_file_name))


def download_model():
    # change these path to your own google cloud storage path
    download_blob('lang_det_model', 'variables/variables.data-00000-of-00001',
                  '/tmp/variables/variables.data-00000-of-00001')
    download_blob('lang_det_model', 'variables/variables.index', '/tmp/variables/variables.index')
    download_blob('lang_det_model', 'saved_model.pb', '/tmp/saved_model.pb')


# Define and map your model's output here
def handler(request):
    global model
    lang_labels = {
        0: "eng",
        1: "malay",
        2: "rojak",
        3: "manglish",
        4: "other"
    }

    if load_model_at_local:
        try:
            # model = tf.saved_model.load('/models/yourmodelpath')
            model = tf.saved_model.load('../../models/lang_det_model')
        except Exception as ecx:
            print(ecx)
    # Model load which only happens during cold starts
    if model is None:
        download_model()
        model = tf.saved_model.load('/tmp')

    request_json = request.get_json(silent=True)
    input_txt = request_json['text']
    session_name = request_json['sessionInfo']['session']
    # for our example, we have our tokenizer saved inside our model,
    # you might need to change this line based on your model's input shape or add extra lines if you need a separate function to tokenize your text
    preds = model([[input_txt]])
    # get prediction scores
    preds = tf.squeeze(preds, axis=0).numpy()
    jsonResponse = {
        "session_info": {
            "session": session_name,
            "parameters": {
                "language": lang_labels[preds.argmax()]
            }
        }
    }
    return jsonResponse
