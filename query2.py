from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['qlhs']
students_collection = db['hoc_sinh']

@app.route('/students', methods=['GET'])
def get_students():
    """Lấy danh sách học sinh với tùy chọn lọc theo giới tính hoặc lớp và phân trang."""
    gender = request.args.get('gender')
    class_name = request.args.get('class')
    student_id = request.args.get('id')  # Thêm tham số id để tìm học sinh cụ thể
    per_page = int(request.args.get('per_page', 10))  # Số lượng học sinh trên mỗi trang, mặc định là 10
    
    # Tạo query cho việc lọc học sinh
    query = {}
    if gender:
        query['gioi_tinh'] = gender
    if class_name:
        query['lop'] = class_name

    # Lấy tổng số học sinh theo query
    student_total = students_collection.count_documents(query)

    # Tính toán tổng số trang
    page_total = (student_total + per_page - 1) // per_page  # Tổng số trang

    # Lấy giá trị của page từ request, mặc định là 1
    page = int(request.args.get('page', 1))

    # Nếu có student_id, tìm kiếm vị trí của học sinh đó trong tập dữ liệu
    if student_id:
        student = students_collection.find_one({'_id': student_id})
        if student:
            # Tính toán trang mà học sinh cụ thể sẽ thuộc về
            student_position = students_collection.count_documents(query) - students_collection.count_documents(query, {'_id': {'$gt': student_id}})
            page = (student_position // per_page) + 1

    # Kiểm tra và điều chỉnh page nếu cần
    if page < 1:
        page = 1
    elif page > page_total and page_total > 0:
        page = page_total

    # Tính toán số lượng bản ghi cần bỏ qua
    skip = (page - 1) * per_page
    students = list(students_collection.find(query).skip(skip).limit(per_page))

    return jsonify({
        "student_total": student_total,  # Đổi tên trường thành student_total
        "page_total": page_total,         # Thêm trường page_total
        "page": page,
        "per_page": per_page,
        "students": students
    })

if __name__ == '__main__':
    app.run(debug=True)
