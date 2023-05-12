from flask import Flask, render_template

app = Flask(__name__)

student_data = {
    1: {"name": "노무현", "score": {"국어": 5, "수학":  23}},
    2: {"name": "전두환", "score": {"국어": 5, "수학":  18}}
}
@app.route('/')
def index():
    return render_template("index.html",
                           template_students = student_data)

@app.route('/student/<int:id>')
def user(id):
    return render_template("student.html",
                           template_students = student_data[id]["name"],
                           template_score=student_data[id]["score"])

if __name__ == '__main__':
    app.run(debug=True)