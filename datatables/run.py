from flask import Flask, render_template
from flask_wtf import Form
from wtforms.fields.html5 import DateField
app = Flask(__name__)
app.secret_key = 'SHH!'


class ExampleForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')


@app.route('/', methods=['POST','GET'])
def hello_world():
    form = ExampleForm()
    if form.validate_on_submit():
        return form.dt.data.strftime('%Y-%m-%d')
    return render_template('example.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)