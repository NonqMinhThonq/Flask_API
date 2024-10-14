from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['qlhs']
students_collection = db['hoc_sinh']

# Thêm học sinh mới
@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    student_id = int(data['_id'])  # Chuyển đổi sang số nguyên

    # Kiểm tra xem _id đã tồn tại chưa
    if students_collection.find_one({"_id": student_id}):
        return jsonify({"message": "ID bị trùng"}), 400  # Trả về mã lỗi 400

    student = {
        "_id": student_id,  # Sử dụng student_id đã chuyển đổi
        "ho_ten": data.get('ho_ten'),
        "lop": data.get('lop'),
        "gioi_tinh": data.get('gioi_tinh'),
        "dia_chi": data.get('dia_chi')
    }
    students_collection.insert_one(student)
    return jsonify({"message": "Student added successfully!"}), 201

@app.route('/students/<int:id_hocsinh>', methods=['GET'])
def get_student(id_hocsinh):
    student = students_collection.find_one({"_id": id_hocsinh})
    if student:
        student['_id'] = str(student['_id'])  # Convert ObjectId to string if needed
        return jsonify(student), 200
    else:
        return jsonify({"error": "Student not found"}), 404

# Cập nhật thông tin học sinh
@app.route('/students/<int:id_hocsinh>', methods=['PUT'])
def update_student(id_hocsinh):
    data = request.json
    student = students_collection.find_one({"_id": id_hocsinh})

    if not student:
        return jsonify({"message": "Student not found"}), 404

    # Kiểm tra nếu người dùng cố gắng thay đổi _id
    if '_id' in data and data['_id'] != id_hocsinh:
        return jsonify({"message": "Cannot change student ID"}), 400

    # Cập nhật các trường thông tin
    updated_student = {
        "ho_ten": data.get('ho_ten', student['ho_ten']),
        "lop": data.get('lop', student['lop']),
        "gioi_tinh": data.get('gioi_tinh', student['gioi_tinh']),
        "dia_chi": data.get('dia_chi', student['dia_chi'])
    }

    students_collection.update_one({"_id": id_hocsinh}, {"$set": updated_student})
    return jsonify({"message": "Student updated successfully!"}), 200
# Xóa học sinh
@app.route('/students/<int:id_hocsinh>', methods=['DELETE'])
def delete_student(id_hocsinh):
    result = students_collection.delete_one({"_id": id_hocsinh})
    if result.deleted_count:
        return jsonify({"message": "Student deleted successfully!"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
