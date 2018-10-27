import exifread, requests, os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

clarifai = ClarifaiApp(api_key='YOUR_API_KEY')
clarifai_model = clarifai.models.get('general-v1.3')

# For later use
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

UPLOAD_FOLDER = './uploads'
clarifai_tags = []

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploadImage', methods=['GET', 'POST'])
def imageUpload():
    if request.method == 'POST':
        f = request.files['image']
        name = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], name))

        # ClarifAI
        clarifai_image = ClImage(file_obj=open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb'))
        clarifai_prediction = clarifai_model.predict([clarifai_image])
        clarifai_data = clarifai_prediction['outputs'][0]['data']['concepts']

        for tags in clarifai_data:
            clarifai_tags.append(tags['name'].title())
        print "Tags: " + clarifai_tags

        # EXIF Meta Data
        open_image = open(os.path.join(app.config['UPLOAD_FOLDER'], name), 'rb')
        exif_tags = exifread.process_file(open_image)

        for tag in exif_tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                camera_make = str(exif_tags['Image Make'])
                camera_model = str(exif_tags['Image Model'])
                lens_make = str(exif_tags['EXIF LensMake'])
                lens_model = str(exif_tags['EXIF LensModel'])
                image_time = str(exif_tags['EXIF DateTimeOriginal'])
                image_software = str(exif_tags['Image Software'])
                image_aperture = str(exif_tags['EXIF ApertureValue'])
                image_shutterspeed = str(exif_tags['EXIF ShutterSpeedValue'])
                image_iso_speed = str(exif_tags['EXIF ISOSpeedRatings'])
                image_brightness = str(exif_tags['EXIF BrightnessValue'])
                image_focal_length = str(exif_tags['EXIF FocalLength'])
                image_f_stop = str(exif_tags['EXIF FNumber'])
                image_white_balance = str(exif_tags['EXIF WhiteBalance'])
                image_color_space = str(exif_tags['EXIF ColorSpace'])
                image_orientation = str(exif_tags['Image Orientation'])
                image_exposure_bias = str(exif_tags['EXIF ExposureBiasValue'])
                image_exposure_time = str(exif_tags['EXIF ExposureTime'])
                image_exposure_mode = str(exif_tags['EXIF ExposureMode'])

    return "Image Uploaded"

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)