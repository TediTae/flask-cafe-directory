from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-for-you'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location Link', validators=[DataRequired(), URL()])
    open = TimeField('Opening Time', validators=[DataRequired()])
    close = TimeField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rate', choices=[('1','☕️'),('2','☕️☕️'),('3','☕️☕️☕️'),('4','☕️☕️☕️☕️'),('5','☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    wifi = SelectField('Wi-Fi Strength', choices=[('1','✘'),('2','💪'),('3','💪💪'),('4','💪💪💪'),('5','💪💪💪💪'),('6','💪💪💪💪💪')], validators=[DataRequired()])
    power = SelectField('Power Rate', choices=[('1','✘'),('2','🔌'),('3','🔌🔌'),('4','🔌🔌🔌'),('5','🔌🔌🔌🔌'),('6','🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add')
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe_name.data
        location = form.location.data
        open_time = form.open.data.strftime("%H:%M")
        close_time = form.close.data.strftime("%H:%M")
        coffee_rate = form.coffee_rating.data
        wifi = form.wifi.data
        power = form.power.data

        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([cafe_name, location, open_time, close_time, coffee_rate, wifi, power])

        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open("cafe-data.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        cafes = list(reader)
    return render_template('cafes.html', cafes=cafes)



if __name__ == '__main__':
    app.run(debug=True)
