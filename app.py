from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_user = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        email_user = request.form.get('email_user')

        search_user = User.query.filter_by(name=name, last_name=last_name).first()

        if search_user:
            return render_template('index.html', content=f'Уже виделись {name}!')
        elif (name and last_name and email_user) == '':
            return render_template('index.html', content='Ошибка! Вы что-то не ввели!')

        user = User(name=name, last_name=last_name, email_user=email_user)

        try:
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            return render_template('index.html', content=f'Привет {name} {last_name}!')
        except:
            return f'Произошла ошибка при добавлении пользователя'
    else:
        return render_template('index.html')


@app.route('/names')
def names():
    users = User.query.all()
    return render_template('names_list.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)