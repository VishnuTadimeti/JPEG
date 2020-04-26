import exifread, requests, os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import matplotlib.pyplot as matplot

clarifai = ClarifaiApp(api_key='bb1c6d463f8040ca94ac3d54ae26702c')
clarifai_model = clarifai.models.get('general-v1.3')

# For later use
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploadImage', methods=['GET', 'POST'])
def imageUpload():
    if request.method == 'POST':
        clarifai_tags = []
        f = request.files['image']
        name = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        print ("Image Path: ", str(image_path))

        # ClarifAI
        clarifai_image = ClImage(file_obj=open(image_path, 'rb'))
        clarifai_prediction = clarifai_model.predict([clarifai_image])
        clarifai_data = clarifai_prediction['outputs'][0]['data']['concepts']
        for tags in clarifai_data:
            clarifai_tags.append(tags['name'].title())
        print ("Tags: ", str(clarifai_tags))

        # MatPlotLib - Generate Histogram
        # matplot_image = matplot.imread(image_path)

        # EXIF Meta Data
        # open_image = open(image_path, 'rb')
        # exif = exifread.process_file(open_image)
        # print("EXIF: ", exif)

        # try:
        #     for exif_tags in exif.keys():
        #         if exif_tags not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        #             camera_make = str(exif_tags['Image Make'])
        #             camera_model = str(exif_tags['Image Model'])
        #             lens_make = str(exif_tags['EXIF LensMake'])
        #             lens_model = str(exif_tags['EXIF LensModel'])
        #             image_time = str(exif_tags['EXIF DateTimeOriginal'])
        #             image_software = str(exif_tags['Image Software'])
        #             image_aperture = str(exif_tags['EXIF ApertureValue'])
        #             image_shutterspeed = str(exif_tags['EXIF ShutterSpeedValue'])
        #             image_iso_speed = str(exif_tags['EXIF ISOSpeedRatings'])
        #             image_brightness = str(exif_tags['EXIF BrightnessValue'])
        #             image_focal_length = str(exif_tags['EXIF FocalLength'])
        #             image_f_stop = str(exif_tags['EXIF FNumber'])
        #             image_white_balance = str(exif_tags['EXIF WhiteBalance'])
        #             image_color_space = str(exif_tags['EXIF ColorSpace'])
        #             image_orientation = str(exif_tags['Image Orientation'])
        #             image_exposure_bias = str(exif_tags['EXIF ExposureBiasValue'])
        #             image_exposure_time = str(exif_tags['EXIF ExposureTime'])
        #             image_exposure_mode = str(exif_tags['EXIF ExposureMode'])
        return render_template('image.html', no_image=False, image_path=name,
                                           tags=clarifai_tags)
        print ("Found everything needed")
        # except:
        #     print ("Something is missing")
        #     return render_template('image.html', no_image=True, message="Something is missing", tags=clarifai_tags, image_path=name)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)