import pymysql
import csv

timeout = 10

def create_table():
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="interview-go-luisaccforwork-9b17.g.aivencloud.com",
        password="AVNS_JAQYYlYjdLqtQoDJM6c",
        read_timeout=timeout,
        port=10460,
        user="avnadmin",
        write_timeout=timeout,
    )
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS mytest (
            sbd INT PRIMARY KEY,
            toan FLOAT,
            ngu_van FLOAT,
            ngoai_ngu FLOAT,
            vat_li FLOAT,
            hoa_hoc FLOAT,
            sinh_hoc FLOAT,
            lich_su FLOAT,
            dia_li FLOAT,
            gdcd FLOAT,
            ma_ngoai_ngu VARCHAR(10)
        )
        """
        cursor.execute(query)
        connection.commit()
    finally:
        connection.close()

def insert_data(data):
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="interview-go-luisaccforwork-9b17.g.aivencloud.com",
        password="AVNS_JAQYYlYjdLqtQoDJM6c",
        read_timeout=timeout,
        port=10460,
        user="avnadmin",
        write_timeout=timeout,
    )
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO mytest (sbd, toan, ngu_van, ngoai_ngu, vat_li, hoa_hoc, sinh_hoc, lich_su, dia_li, gdcd, ma_ngoai_ngu)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(query, data)
        connection.commit()
    finally:
        connection.close()

def read_csv_and_insert_data(csv_filepath):
    data = []
    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                data.append((
                    int(row['sbd']) if row['sbd'] else 0,
                    float(row['toan']) if row['toan'] else 0.0,
                    float(row['ngu_van']) if row['ngu_van'] else 0.0,
                    float(row['ngoai_ngu']) if row['ngoai_ngu'] else 0.0,
                    float(row['vat_li']) if row['vat_li'] else 0.0,
                    float(row['hoa_hoc']) if row['hoa_hoc'] else 0.0,
                    float(row['sinh_hoc']) if row['sinh_hoc'] else 0.0,
                    float(row['lich_su']) if row['lich_su'] else 0.0,
                    float(row['dia_li']) if row['dia_li'] else 0.0,
                    float(row['gdcd']) if row['gdcd'] else 0.0,
                    row['ma_ngoai_ngu'] if row['ma_ngoai_ngu'] else ''
                ))
            except ValueError as e:
                print(f"Skipping row due to data error: {e}")
    insert_data(data)

def find_student_by_sbd(sbd):
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="interview-go-luisaccforwork-9b17.g.aivencloud.com",
        password="AVNS_JAQYYlYjdLqtQoDJM6c",
        read_timeout=timeout,
        port=10460,
        user="avnadmin",
        write_timeout=timeout,
    )
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM mytest WHERE sbd = %s"
        cursor.execute(query, (sbd,))
        result = cursor.fetchone()
        return result
    finally:
        connection.close()

# Example usage:
student = find_student_by_sbd(1000036)
print(student)

