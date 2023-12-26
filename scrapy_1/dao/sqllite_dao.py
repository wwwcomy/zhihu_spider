import sqlite3
from scrapy_1.models.model import CrawlSummary

class SqliteCrawSummaryDao:
    def save_craw_summary(self, crawl_summary: CrawlSummary):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS crawl_summary
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, spider_name text, start_time DATETIME, 
                    end_time DATETIME, data_count int)
                ''')
        c.execute("INSERT INTO crawl_summary (spider_name, start_time, end_time, data_count) VALUES (?, ?, ?, ?)",
                    (crawl_summary.name, crawl_summary.start_time, crawl_summary.end_time, crawl_summary.data_count))
        conn.commit()
        conn.close()

    def list_crawl_summary(self) -> list:
        conn = self.get_conn()
        c = conn.cursor()
        c.execute("SELECT id, spider_name, start_time, end_time, data_count FROM crawl_summary")
        rows = c.fetchall()
        summary_list = []
        for row in rows:
            summary_list.append(CrawlSummary(row[1], row[2], row[3], row[4], row[5]))
        conn.close()
        return summary_list

    def get_conn(self):
        conn = sqlite3.connect('data.db')
        return conn
    
class SqliteHouseInfoDao:
    def save_house_info(self, house_info):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS house_info
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,house_id text, district text, sub_district text,
                    title text, position_id text, position_info text, 
                    house_info text, house_type text, house_area text, house_direction text, 
                    house_decoration text, house_floor text, house_year text, total_price text, unit_price text)
                ''')
        c.execute('''INSERT INTO house_info 
                  (house_id, district, sub_district, title, position_id,
                  position_info, house_info, house_type, house_area, house_direction,
                  house_decoration, house_floor, house_year, total_price, unit_price, 
                  last_update_time) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (house_info.house_id, house_info.district, house_info.sub_district,
                     house_info.title, house_info.position_id, house_info.position_info,
                     house_info.house_info, house_info.house_type, house_info.house_area,
                     house_info.house_direction, house_info.house_decoration, house_info.house_floor,
                     house_info.house_year, house_info.total_price, house_info.unit_price,
                     house_info.last_update_time))
        conn.commit()
        conn.close()

    def get_house_info(self, house_id):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute("SELECT id, house_id, district, sub_district, title, position_id, position_info, house_info, house_type, house_area, house_direction, house_decoration, house_floor, house_year, total_price, unit_price, last_update_time FROM house_info where house_id = ?", (house_id,))
        row = c.fetchone()
        conn.close()
        return row
    
    def update_house_info(self, house_info):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''UPDATE house_info SET district = ?, sub_district = ?, title = ?, position_id = ?, position_info = ?, house_info = ?, house_type = ?, 
                  house_area = ?, house_direction = ?, house_decoration = ?, house_floor = ?, house_year = ?, 
                  total_price = ?, unit_price = ?, last_update_time = ? WHERE house_id = ?''',
                  (house_info.district, house_info.sub_district, house_info.title, house_info.position_id,
                   house_info.position_info, 
                   house_info.house_info, house_info.house_type, 
                   house_info.house_area, house_info.house_direction, house_info.house_decoration, 
                   house_info.house_floor, house_info.house_year, house_info.total_price, 
                   house_info.unit_price, house_info.last_update_time, house_info.house_id))
        conn.commit()
        conn.close()

    
    def get_conn(self):
        conn = sqlite3.connect('data.db')
        return conn
    
