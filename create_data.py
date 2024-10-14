from faker import Faker
from pymongo import MongoClient

fake = Faker()

# Kết nối tới MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['qlhs']
students_collection = db['hoc_sinh']

# Số lượng học sinh muốn fake
NUM_STUDENTS = 50

def create_fake_student(student_id):
    """Tạo một học sinh giả với thông tin ngẫu nhiên"""
    student = {
        "_id": student_id,  # Sử dụng số nguyên làm _id
        "ho_ten": fake.name(),
        "lop": f"{'12'}A{fake.random_int(min=1, max=5)}",
        "gioi_tinh": fake.random_element(elements=('Nam', 'Nu')),
        "dia_chi": fake.random_element(elements=('ha noi', 'cao bang', 'tphcm','da nang'))
    }
    return student

if __name__ == '__main__':
    for i in range(1, NUM_STUDENTS + 1):
        student = create_fake_student(i)
        students_collection.insert_one(student)
        print(f"Added student: {student}")

