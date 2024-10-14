from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['qlhs']
students_collection = db['hoc_sinh']

@app.route('/students/page', methods=['GET'])
def get_students_paginated():
    """Lấy danh sách học sinh với phân trang"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Tính toán chỉ số bắt đầu
    skip = (page - 1) * limit

    students = list(students_collection.find().skip(skip).limit(limit))
    
    return jsonify(students)

@app.route('/students/gender/<gender>', methods=['GET'])
def get_students_by_gender(gender):
    """Lấy danh sách học sinh theo giới tính"""
    students = list(students_collection.find({'gioi_tinh': gender}))
    return jsonify(students)

@app.route('/students/class/<class_name>', methods=['GET'])
def get_students_by_class(class_name):
    """Lấy danh sách học sinh theo lớp"""
    students = list(students_collection.find({'lop': class_name}))
    return jsonify(students)

@app.route('/students/count/gender/<gender>', methods=['GET'])
def get_student_count_by_gender(gender):
    """Lấy số lượng học sinh theo giới tính"""
    count = students_collection.count_documents({'gioi_tinh': gender})
    return jsonify({'count': count})

@app.route('/students', methods=['GET'])
def get_students():
    """Lấy danh sách học sinh với tùy chọn lọc theo giới tính hoặc lớp và phân trang."""
    gender = request.args.get('gender')
    class_name = request.args.get('class')
    page = int(request.args.get('page', 1))  # Trang hiện tại, mặc định là 1
    per_page = int(request.args.get('per_page', 10))  # Số lượng học sinh trên mỗi trang, mặc định là 10

    query = {}
    if gender:
        query['gioi_tinh'] = gender
    if class_name:
        query['lop'] = class_name

    # Lấy tổng số học sinh
    total_students = students_collection.count_documents(query)
    
    # Tính toán số học sinh cần lấy dựa trên phân trang
    skip = (page - 1) * per_page
    students = list(students_collection.find(query).skip(skip).limit(per_page))
    
    return jsonify({
        "total": total_students,
        "page": page,
        "per_page": per_page,
        "students": students
    })

if __name__ == '__main__':
    app.run(debug=True)
