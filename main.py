import os
from flask_wtf.form import FlaskForm
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from wtforms import SubmitField
from flask_bootstrap import Bootstrap
from wtforms.fields.core import SelectField
from extract_color import ExtractColor
from dotenv import load_dotenv

load_dotenv('portfolio_projects\Color Extractor\.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
Bootstrap(app)
filepath = ""


class UploadImageForm(FlaskForm):
    color_choice = [(5, '5'), (10, '10'), (15, '15')]
    
    image_file = FileField("Upload File", validators=[
        FileRequired(),
        FileAllowed(upload_set=['jpg', 'png'], message="Images only!")
    ])
    num_of_colors = SelectField('Number of Colors', choices=color_choice)
    extract = SubmitField("Extract Colors")


@app.route("/", methods=["GET", "POST"])
def home():
    """Home page with a wtf quick form"""
    upload_form = UploadImageForm()
    if request.method == "POST" and upload_form.validate_on_submit():
        file = upload_form.image_file.data
        col_number = int(upload_form.num_of_colors.data)

        # Alternate way to extract filename
        # f = request.files['image_file']
        # print(f.filename)

        filename = file.filename
        filepath = os.path.join(
            'static/assets/images/uploads', filename
        )
        try:
            file.save(filepath)
        except AttributeError:
            print("Select an image!")
        extracted_colors = ExtractColor().extract_colors(filepath, col_number)
        image = "assets/images/uploads/"+filename
        return render_template("index.html", form=upload_form, image=image, extracted_colors=extracted_colors)
    else:
        filepath = "assets/images/initial_upload/6.jpg"
        return render_template("index.html", form=upload_form, image=filepath, extracted_colors=[])


if __name__ == "__main__":
    app.run(debug=True)


