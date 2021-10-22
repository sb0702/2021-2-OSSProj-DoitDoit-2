import pymysql
import bcrypt



class Database:
    def __init__():
        score_db = pymysql.connect(
            user='admin',
            password='tjgus1234',
            host='mytetris.cw4my8jpnexs.ap-northeast-2.rds.amazonaws.com',
            db='tetris',
            charset='utf8'
        )

    def id_not_exists(input_id, mode): # 아이디가 데이터베이스에 존재하는지 확인
        curs = score.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM mode WHERE id=%s"
        curs.execute(sql, input_id)
        data = curs.fetchone()
        curs.close()
        if data:
            return False
        else:
            return True

    def add_id_data(user_id): # 아이디 추가
        #추가하기
        curs = score.cursor()
        sql = "INSERT INTO users (user_id) VALUES (%s)"
        curs.execute(sql, user_id)
        self.score_db.commit()  #서버로 추가 사항 보내기
        curs.close()


    def add_data(game_mode,  id, score):
        #추가하기
        curs = score.cursor()
        if game_mode == 'Normal':
            sql = "INSERT INTO Normal (id, score) VALUES (%s, %s)"
        elif game_mode == 'Hard':
            sql = "INSERT INTO Hard (id, score) VALUES (%s, %s)"
        elif game_mode == 'Reverse':
            sql = "INSERT INTO Reverse (id, score) VALUES (%s, %s)"
        elif game_mode == 'Item':
            sql = "INSERT INTO Item (id, score) VALUES (%s, %s)"
        
        curs.execute(sql, (id, score))
        tetris_db.commit()  #서버로 추가 사항 보내기
        curs.close()
