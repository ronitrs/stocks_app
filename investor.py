# Class for Investor
class Investor:
    def __init__(self, investor_id, name, address, phone_number):
        self.investor_id = investor_id
        self.name = name
        self.address = address
        self.phone_number = phone_number
    stocks = []
    bonds = []