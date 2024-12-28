from flask import Flask, render_template, request, send_file, jsonify
import pymysql
import matplotlib
# Đặt backend 'Agg' trước khi import pyplot
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from models.subject_manager import SubjectManager

app = Flask(__name__)
subject_manager = SubjectManager()

# Configure MySQL connection
db_config = {
    'charset': 'utf8mb4',
    'connect_timeout': 10,
    'cursorclass': pymysql.cursors.DictCursor,
    'db': 'defaultdb',
    'host': 'interview-go-luisaccforwork-9b17.g.aivencloud.com',
    'password': 'AVNS_JAQYYlYjdLqtQoDJM6c',
    'port': 10460,
    'user': 'avnadmin',
    'read_timeout': 10,
    'write_timeout': 10,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    sbd = request.form['sbd']
    connection = pymysql.connect(**db_config)
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM mytest WHERE sbd = %s"
        cursor.execute(query, (sbd,))
        result = cursor.fetchone()
    finally:
        connection.close()
    
    if result:
        return render_template('index.html', student=result)
    else:
        return render_template('index.html', no_result=True)

@app.route('/report')
def report():
    # Lấy tham số môn học từ URL, nếu không có thì hiển thị tất cả
    subject = request.args.get('subject', 'all')
    
    # Dictionary ánh xạ tên hiển thị và tên cột trong DB
    subject_mapping = {
        'toan': 'Toán',
        'ngu_van': 'Ngữ Văn',
        'ngoai_ngu': 'Ngoại Ngữ',
        'vat_li': 'Vật Lý',
        'hoa_hoc': 'Hóa Học',
        'sinh_hoc': 'Sinh Học',
        'lich_su': 'Lịch Sử',
        'dia_li': 'Địa Lý',
        'gdcd': 'GDCD'
    }

    connection = pymysql.connect(**db_config)
    try:
        cursor = connection.cursor()
        
        # Tối ưu query dựa trên môn học được chọn
        if subject != 'all' and subject in subject_mapping:
            query = f"SELECT {subject} FROM mytest WHERE {subject} IS NOT NULL"
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Chuyển đổi kết quả thành list điểm
            scores = [row[subject] for row in results]
            
            # Thống kê cho một môn
            levels = {
                '>=8 điểm': [sum(1 for score in scores if score >= 8)],
                '6-8 điểm': [sum(1 for score in scores if 6 <= score < 8)],
                '4-6 điểm': [sum(1 for score in scores if 4 <= score < 6)],
                '<4 điểm': [sum(1 for score in scores if score < 4)]
            }
            subjects = [subject_mapping[subject]]
            
        else:
            # Nếu xem tất cả các môn
            columns = list(subject_mapping.keys())
            columns_str = ', '.join(columns)
            query = f"SELECT {columns_str} FROM mytest"
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Thống kê cho tất cả các môn
            levels = {
                '>=8 điểm': [],
                '6-8 điểm': [],
                '4-6 điểm': [],
                '<4 điểm': []
            }
            
            for col in columns:
                scores = [row[col] for row in results if row[col] is not None]
                levels['>=8 điểm'].append(sum(1 for score in scores if score >= 8))
                levels['6-8 điểm'].append(sum(1 for score in scores if 6 <= score < 8))
                levels['4-6 điểm'].append(sum(1 for score in scores if 4 <= score < 6))
                levels['<4 điểm'].append(sum(1 for score in scores if score < 4))
            
            subjects = list(subject_mapping.values())
            
    finally:
        connection.close()

    if not results:
        return render_template('report.html', no_data=True)

    # Tạo biểu đồ
    plt.figure(figsize=(10, 6))
    bar_width = 0.2
    x = range(len(subjects))

    # Vẽ biểu đồ cột cho từng cấp độ
    plt.bar([p - bar_width*1.5 for p in x], levels['>=8 điểm'], width=bar_width, label='>=8 điểm', color='green')
    plt.bar([p - bar_width/2 for p in x], levels['6-8 điểm'], width=bar_width, label='6-8 điểm', color='blue')
    plt.bar([p + bar_width/2 for p in x], levels['4-6 điểm'], width=bar_width, label='4-6 điểm', color='orange')
    plt.bar([p + bar_width*1.5 for p in x], levels['<4 điểm'], width=bar_width, label='<4 điểm', color='red')

    # Thiết lập các thuộc tính biểu đồ
    plt.xticks(x, subjects, rotation=45)
    plt.title(f'Phân loại điểm{" môn " + subject_mapping[subject] if subject != "all" else ""}', fontsize=16)
    plt.xlabel('Môn học', fontsize=12)
    plt.ylabel('Số lượng học sinh', fontsize=12)
    plt.legend()
    plt.tight_layout()

    # Lưu biểu đồ vào buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png')

@app.route('/report-page')
def report_page():
    subject_mapping = {
        'toan': 'Toán',
        'ngu_van': 'Ngữ Văn',
        'ngoai_ngu': 'Ngoại Ngữ',
        'vat_li': 'Vật Lý',
        'hoa_hoc': 'Hóa Học',
        'sinh_hoc': 'Sinh Học',
        'lich_su': 'Lịch Sử',
        'dia_li': 'Địa Lý',
        'gdcd': 'GDCD'
    }
    return render_template('report.html', subjects=subject_mapping)

@app.route('/top-students')
def top_students_page():
    blocks_info = subject_manager.get_blocks_for_display()
    return render_template('top_students.html', blocks=blocks_info)

@app.route('/api/top-students')
def get_top_students():
    block_code = request.args.get('block', 'A00')
    
    if block_code not in subject_manager.get_all_blocks():
        return jsonify({'error': 'Khối thi không hợp lệ'}), 400
        
    subject_cols = subject_manager.get_block_subjects(block_code)
    
    connection = pymysql.connect(**db_config)
    try:
        cursor = connection.cursor()
        select_cols = ', '.join(subject_cols)
        sum_formula = f"({' + '.join(subject_cols)}) as total_score"
        
        query = f"""
        SELECT sbd, {select_cols}, {sum_formula}
        FROM mytest
        WHERE {' AND '.join(f'{col} IS NOT NULL' for col in subject_cols)}
        ORDER BY total_score DESC
        LIMIT 10
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        return jsonify({
            'data': results,
            'subjects': subject_cols
        })
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
