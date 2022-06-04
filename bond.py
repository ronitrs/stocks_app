from .stock import Stock
# Inherit Bond class from Stock
class Bond(Stock):
    def __init__(self, stock_id, symbol, quantity, purchase_price, current_value, purchase_date, coupon, _yield):
        super().__init__(stock_id, symbol, quantity, purchase_price, current_value, purchase_date)
        self.coupon = coupon
        self._yield = _yield