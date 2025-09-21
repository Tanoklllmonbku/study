from flask import Flask, request

app = Flask(__name__)

students = [
    {
        "id": 1,
        "name": "Govnoed",
        "lastname": "Asinskiy",
        "faculity": "SmellySocksProgrammer"
    },
    {
        "id": 3,
        "name": "Govnoed",
        "lastname": "Asinskiy",
        "faculity": "SmellySocksProgrammer"
    }
]


@app.route("/govnoedy/<int:id>", methods=["GET"])
def get_stud(id):
    student = list(filter(lambda x: x["id"] == id, students))
    if len(student) != 0:
        return f"Hello, {student}"
    else:
        return "Otsosi"


@app.route("/govnoedy/<int:id>", methods=["POST"])
def post_stud(id):
    data = {
        "name": request.json["name"],
        "lastname": request.json["lastname"],
        "faculity": request.json["faculity"]
    }
    data["id"] = int(id)
    students.append(data)
    return students[id]


@app.route("/govnoedy", methods=["GET"])
def get_studs():
    students_name = []
    for i in range(len(students)):
        students_name.append(students[i]["name"])

    return "\n".join(students_name)


@app.route("/govnoedy/delete/<int:id>", methods=["GET"])
def del_stud(id):
    global students
    for i in range(len(students)):
        if students[i]["id"] != int(id):
            return "Otsosi"
        else:
            students = [student for student in students if student["id"] != int(id)]
            return students


if __name__ == "__main__":
    app.run(port=8082)
