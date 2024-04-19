import sys,os
from isd.pipeline.training_pipeline import TrainPipeline
from isd.utils.main_utils import decodeImage, encodeImageIntoBase64
from flask import Flask, request, jsonify, render_template,Response
from flask_cors import CORS, cross_origin
from isd.configuration.s3_operations import S3Operation
from isd.entity.config_entity import ModelPusherConfig
from isd.exception import isdException
from isd.logger import logging

# initialize flask app
app = Flask(__name__)
CORS(app)

# user provide image
class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        



@app.route("/train")
def trainRoute():
    obj = TrainPipeline()
    obj.run_pipeline()
    return 
    

# render home page
@app.route("/")
def home():
    return render_template("index.html")

# After training, best.pt is saved to yolov7 dir; since it's cloned dir from other source, it won't be pushed to Github repo. 
# best.pt won't be available for making pred's in cloud. So, we need to get model from s3
def download_model_from_S3() -> str:
    """
    Fetch model from s3
    """
    try:
        # can get model name from model_pusher config
        model_pusher_config= ModelPusherConfig()
        s3= S3Operation()
        
        # to where s3 model can be downloaded
        download_model_dir = 'yolov7' + "/" + model_pusher_config.S3_MODEL_KEY_PATH # yolov7/best.pt
        
        # if model available ok, else download from s3
        if os.path.exists(download_model_dir):
            logging.info(f"Model file already exist: {download_model_dir}")
            
        else: 
            # Download the file from S3 bucket
            s3.download_object(key= model_pusher_config.S3_MODEL_KEY_PATH,
                           bucket_name= model_pusher_config.MODEL_BUCKET_NAME,
                           filename= download_model_dir)
            
            logging.info(f"Model file successfully downloaded from S3 bucket: {model_pusher_config.MODEL_BUCKET_NAME}/{model_pusher_config.S3_MODEL_KEY_PATH}")
        return model_pusher_config.S3_MODEL_KEY_PATH
            
    except Exception as e:
            raise isdException(e, sys) from e 
        

@app.route("/predict", methods=['POST','GET'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        # decode image
        decodeImage(image, clApp.filename)
        
        # get the trained model from s3 bucket
        model_file = download_model_from_S3()
        logging.info(f"downloaded model file from S3 bucket!")
       
       #  running detect.py by loading model saved in yolov7 dir
        os.system("cd yolov7/ && python detect.py --weights best.pt  --source ../data/inputImage.jpg")

        opencodedbase64 = encodeImageIntoBase64("yolov7/runs/detect/exp/inputImage.jpg")
        result = {"image": opencodedbase64.decode('utf-8')}
        os.system("rm -rf yolov7/runs")

    except ValueError as val:
        print(val)
        return Response("Value not found inside  json data")
    except KeyError:
        return Response("Key value error incorrect key passed")
    except Exception as e:
        print(e)
        result = "Invalid input"

    return jsonify(result)


if __name__ == "__main__":
    clApp = ClientApp()
    app.run(host="0.0.0.0", port=1111)
    