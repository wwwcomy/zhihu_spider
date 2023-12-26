
from datetime import datetime

class CrawlSummary:
    def __init__(self, id, name, start_time, end_time, data_count):
        self.id = id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.data_count = data_count

    def __str__(self):
        return f'CrawlSummary: {self.name}, {self.start_time}, {self.end_time}, {self.data_count}'


class HouseInfo:
    def __init__(self, id, house_id, district, sub_district, title, position_id, position_info,
                 house_info, house_type, house_area, house_direction, house_decoration,
                 house_floor, house_year, total_price, unit_price, job_time):
        self.id = id
        self.house_id = house_id
        self.district = district
        self.sub_district = sub_district
        self.title = title
        self.position_id = position_id
        self.position_info = position_info
        self.house_info = house_info
        self.house_type = house_type
        self.house_area = house_area
        self.house_direction = house_direction
        self.house_decoration = house_decoration
        self.house_floor = house_floor
        self.house_year = house_year
        self.total_price = total_price
        self.unit_price = unit_price
        self.last_update_time = job_time

    def generate_price_change_history(self, another_house_info, job_time):
        if self.total_price != another_house_info.total_price or self.unit_price != another_house_info.unit_price:
            return HousePriceChangeHistory(None, self.house_id, self.total_price, self.unit_price, job_time)
        else:
            return None

    def __str__(self):
        return f'HouseInfo: {self.title}, {self.position_id}, {self.position_info}, {self.house_id}, {self.house_info}, {self.house_type}, {self.house_area}, {self.house_direction}, {self.house_decoration}, {self.house_floor}, {self.house_year}, {self.total_price}, {self.unit_price}'


class HousePriceChangeHistory:
    def __init__(self, id, house_id, original_total_price, original_unit_price,
                 total_price, unit_price, job_time):
        self.id = id
        self.house_id = house_id
        self.original_total_price = original_total_price
        self.original_unit_price = original_unit_price
        self.total_price = total_price
        self.unit_price = unit_price
        self.change_type = 'down' if self.original_unit_price>self.unit_price else 'up'
        self.change_amount = self.original_unit_price - self.unit_price
        self.job_time = job_time

    def __str__(self):
        return f'HousePriceChangeHistory: {self.house_id}, {self.total_price}, {self.unit_price}, {self.last_update_time}'