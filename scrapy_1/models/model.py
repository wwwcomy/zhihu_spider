from decimal import Decimal

class CrawlSummary:
    def __init__(self, id, name, job_date, start_time, end_time, data_count,
                 new_data_count, price_higher_count, price_lower_count):
        self.id = id
        self.name = name
        self.job_date = job_date
        self.start_time = start_time
        self.end_time = end_time
        self.data_count = data_count
        self.new_data_count = new_data_count
        self.price_higher_count = price_higher_count
        self.price_lower_count = price_lower_count


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
        self.last_update_date = job_time

    def generate_price_change_history(self, another_house_info, job_time):
        if self.total_price != another_house_info.total_price or self.unit_price != another_house_info.unit_price:
            return HousePriceChangeHistory(None, self.house_id, self.total_price, self.unit_price, 
                                           another_house_info.total_price, another_house_info.unit_price, job_time)
        else:
            return None

    def __str__(self):
        return f'HouseInfo: {self.house_id}, {self.total_price}, {self.unit_price}, {self.last_update_date}'

class HousePriceChangeHistory:
    def __init__(self, id, house_id, original_total_price, original_unit_price,
                 total_price, unit_price, job_time):
        self.id = id
        self.house_id = house_id
        self.original_total_price = original_total_price
        self.original_unit_price = original_unit_price
        self.new_total_price = total_price
        self.new_unit_price = unit_price
        self.change_type = 'down' if Decimal(self.original_unit_price) > Decimal(self.new_unit_price) else 'up'
        self.changed_total_amount = Decimal(self.new_total_price) - Decimal(self.original_total_price)
        self.changed_unit_amount = Decimal(self.new_unit_price) - Decimal(self.original_unit_price)
        self.job_time = job_time

    def __str__(self):
        return f'''HousePriceChangeHistory: {self.house_id}, {self.change_type}, 
        {self.changed_total_amount}, {self.changed_unit_amount},
        {self.original_total_price}, {self.original_unit_price}, 
        {self.new_total_price}, {self.new_unit_price}, {self.job_time}'''