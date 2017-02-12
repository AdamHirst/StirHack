import mysql.connector

class Db:

    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost',database='test',user='root',password='pass')

    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        self.conn.commit()

        return result

    def insert_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor

    def add_store(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Store VALUES (NULL)")
        self.conn.commit()
        return cursor.lastrowid

    def add_camera(self, store_id):
        query = "INSERT INTO Camera VALUES (NULL, %s)"
        return self.insert_query(query, (store_id,)).lastrowid

    def add_new_unique_person(self, aws_face_id):
        return self.insert_query("INSERT INTO Person VALUES (NULL, %s)", (aws_face_id, )).lastrowid

    def add_aws_indexed_person(self, person_id, aws_image_id):
        query = "INSERT INTO AwsIndexedPerson VALUES (NULL, %s, %s)"
        return self.insert_query(query, (person_id, aws_image_id,)).lastrowid

    def add_person_occurance(self, store_id, camera_id, timestamp, person_id):
        query = "INSERT INTO PersonOccurrence VALUES (NULL, %s, %s, %s, %s)"
        return self.insert_query(query, (store_id, camera_id, timestamp, person_id,)).lastrowid

    def person_id_from_face_id(self, aws_face_id):
        query = "SELECT id FROM Person WHERE aws_face_id = %s"
        result = self.execute_query(query, (aws_face_id,))
        if len(result) == 0:
            return None
        return result[0][0]

    def remove_close_occurences(self, min_seconds_apart):
        query = """
        delete from personoccurrence where id in  (
            select A.id as id FROM (select * from personoccurrence) as A, (select * from personoccurrence) as B
                where A.id <> B.id
                  and A.id > b.id
                  and A.person_id = B.person_id
                  and abs(unix_timestamp(A.occurance_timestamp)- unix_timestamp(B.occurance_timestamp)) < %s)"""

        self.execute_query(query, (min_seconds_apart, ))

    def occurence_frequency(self, start_timestamp, end_timestamp):
        query = """
        select person_id, count(person_id) as 'freq' from personoccurrence
            where store_id = 1
              and occurance_timestamp >= %s and occurance_timestamp <= %s
            group by person_id
        """

        res = self.execute_query(query, (start_timestamp, end_timestamp, ))
        freq ={}
        for entry in res:
            freq[entry[0]] = entry[1]
        return freq


