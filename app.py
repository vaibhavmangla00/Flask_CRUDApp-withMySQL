from pydoc import describe
from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin123'
app.config['MYSQL_DATABASE_DB'] = 'todo'
mysql.init_app(app)


class Todo:
    def __init__(self):
        # Creating Table
        create_table = '''
        CREATE TABLE if not exists todos(
            sno INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(255) NOT NULL,
            date_created TIMESTAMP DEFAULT NOW()
        );
        '''
        try:
            conn = mysql.connect()
            db = conn.cursor()  # Connecting
            db.execute(create_table)
        except Exception as e:
            print(e)
        finally:
            db.close()
            conn.close()

    def create_todo(self, title, description):
        self.title = title
        self.description = description

        # Connecting with Database
        conn = mysql.connect()
        db = conn.cursor()

        # Command for Inserting
        db.execute('INSERT INTO todos(title, description)\
        VALUES("%s", "%s");' % (title, description))
        conn.commit()  # commit for inserting

    def delete_todo(self, sno):
        self.sno = sno

        conn = mysql.connect()
        db = conn.cursor()

        db.execute('delete from todos where sno="%s";' % (self.sno))
        conn.commit()  # commit for inserting

    def update_todo(self, sno, new_title, new_description):
        self.sno = sno
        self.new_title = new_title
        self.new_description = new_description

        conn = mysql.connect()
        db = conn.cursor()

        db.execute('update todos set title="%s",description="%s" where sno="%s";' % (
            self.new_title, self.new_description, self.sno))
        conn.commit()  # commit for inserting


# CREATE & READ


@app.route('/', methods=['GET', 'POST'])  # add methods when posting
def home():
    conn = mysql.connect()
    db = conn.cursor()

    if request.method == 'POST':
        # print(request.form['title'])
        title = request.form['title']
        description = request.form['description']
        todo.create_todo(title, description)

    # Fetching Data
    db.execute('SELECT * FROM todos;')
    data = db.fetchall()
    return render_template('index.html', data=data)


# DELETE


@app.route('/delete/<int:sno>', methods=['POST', 'GET'])
def delete(sno):
    todo.delete_todo(sno)
    return redirect('/')


# UPDATE


@app.route('/update/<int:sno>', methods=['get', 'post'])
def update(sno):
    conn = mysql.connect()
    db = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        todo.update_todo(sno, title, description)
        return redirect('/')

    db.execute('select * from todos where sno="%s";' % (sno))
    data = db.fetchone()
    return render_template('update.html', data=data)


if __name__ == "__main__":
    todo = Todo()
    app.run(debug=True)
