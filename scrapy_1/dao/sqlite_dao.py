import sqlite3
from scrapy_1.models.model import CrawlSummary
from scrapy_1.models.model import HouseInfo

class SqliteCrawSummaryDao:
    def save_craw_summary(self, crawl_summary: CrawlSummary):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS crawl_summary
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, spider_name text, job_date text,
                    start_time DATETIME, 
                    end_time DATETIME, data_count int, new_data_count int,
                    price_higher_count int, price_lower_count int)
                ''')
        c.execute('''INSERT INTO crawl_summary (spider_name, job_date, start_time, end_time,
                  data_count, new_data_count,
                  price_higher_count, price_lower_count)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                    (crawl_summary.name, crawl_summary.job_date, crawl_summary.start_time, crawl_summary.end_time,
                     crawl_summary.data_count, crawl_summary.new_data_count, crawl_summary.price_higher_count, crawl_summary.price_lower_count))
        conn.commit()
        conn.close()

    def get_conn(self):
        conn = sqlite3.connect('data.db')
        return conn
    
class SqliteHouseInfoDao:
    def save_house_info(self, house_info):
        conn = self.get_conn()
        c = conn.cursor()
        # c.execute('''CREATE TABLE IF NOT EXISTS house_info
        #             (id INTEGER PRIMARY KEY AUTOINCREMENT,house_id text, district text, sub_district text,
        #             title text, position_id text, position_info text, 
        #             house_info text, house_type text, house_area text, house_direction text, 
        #             house_decoration text, house_floor text, house_year text, total_price text, unit_price text,
        #             last_update_date text)
        #         ''')
        c.execute('''INSERT INTO house_info 
                  (house_id, district, sub_district, title, position_id,
                  position_info, house_info, house_type, house_area, house_direction,
                  house_decoration, house_floor, house_year, total_price, unit_price, 
                  last_update_date) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (house_info.house_id, house_info.district, house_info.sub_district,
                     house_info.title, house_info.position_id, house_info.position_info,
                     house_info.house_info, house_info.house_type, house_info.house_area,
                     house_info.house_direction, house_info.house_decoration, house_info.house_floor,
                     house_info.house_year, house_info.total_price, house_info.unit_price,
                     house_info.last_update_date))
        conn.commit()
        conn.close()

    def get_house_info(self, house_id) -> HouseInfo:
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''SELECT id, house_id, district, sub_district, title, 
                  position_id, position_info, house_info, house_type, house_area, 
                  house_direction, house_decoration, house_floor, house_year, total_price, 
                  unit_price, last_update_date FROM house_info where house_id = ?''', (house_id,))
        row = c.fetchone()
        conn.close()
        if row is None:
            return None
        house_info = HouseInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                               row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16])
        return house_info
    
    def update_house_info(self, house_info):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''UPDATE house_info SET district = ?, sub_district = ?, title = ?, position_id = ?, position_info = ?, house_info = ?, house_type = ?, 
                  house_area = ?, house_direction = ?, house_decoration = ?, house_floor = ?, house_year = ?, 
                  total_price = ?, unit_price = ?, last_update_date = ? WHERE house_id = ?''',
                  (house_info.district, house_info.sub_district, house_info.title, house_info.position_id,
                   house_info.position_info, 
                   house_info.house_info, house_info.house_type, 
                   house_info.house_area, house_info.house_direction, house_info.house_decoration, 
                   house_info.house_floor, house_info.house_year, house_info.total_price, 
                   house_info.unit_price, house_info.last_update_date, house_info.house_id))
        conn.commit()
        conn.close()

    def update_house_price(self, house_info, last_update_date):
        conn = self.get_conn()
        c = conn.cursor()
        try:
            c.execute('''UPDATE house_info SET total_price = ?, unit_price = ?, last_update_date = ? WHERE house_id = ?''',
                    (house_info.total_price, house_info.unit_price, last_update_date, house_info.house_id))
            print(f"update_house_price count: {c.rowcount}, house_id: {house_info.house_id}")
            conn.commit()
        except Exception as e:
            print(f"update_house_price error: {e}")
        finally:
            conn.close()

    def update_last_update_date(self, house_info, last_update_date):
        conn = self.get_conn()
        c = conn.cursor()
        try:
            c.execute('''UPDATE house_info SET last_update_date = ? WHERE house_id = ?''',
                    (last_update_date, house_info.house_id))
            print(f"update_last_update_date count: {c.rowcount}, house_id: {house_info.house_id}")
            conn.commit()
        except Exception as e:
            print(f"update_last_update_date error: {e}")
        finally:
            conn.close()

    def get_conn(self):
        conn = sqlite3.connect('data.db')
        return conn

class HousePriceChangeHistoryDao:
    def save_house_price_change_history(self, house_price_change_history):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS house_price_change_history
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, house_id text, house_area text, original_total_price text, original_unit_price text,
                    new_total_price text, new_unit_price text, change_type text, changed_total_amount text, changed_unit_amount text,
                    job_time text)
                ''')
        c.execute('''INSERT INTO house_price_change_history 
                  (house_id, house_area, original_total_price, original_unit_price, new_total_price, new_unit_price,
                  change_type, changed_total_amount, changed_unit_amount, job_time) 
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (house_price_change_history.house_id, house_price_change_history.house_area, house_price_change_history.original_total_price,
                   house_price_change_history.original_unit_price, house_price_change_history.new_total_price,
                   house_price_change_history.new_unit_price, house_price_change_history.change_type,
                   house_price_change_history.changed_total_amount, house_price_change_history.changed_unit_amount,
                   house_price_change_history.job_time))
        conn.commit()
        conn.close()

    def get_conn(self):
        conn = sqlite3.connect('data.db')
        return conn