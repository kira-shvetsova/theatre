
class PricingStrategy:
    def calculate_price(self, base_price, seat):
        return base_price


class RegularPricing(PricingStrategy):
    def calculate_price(self, base_price, seat):
        return base_price * seat.price_coefficient


class DiscountPricing(PricingStrategy):
    def calculate_price(self, base_price, seat):
        return base_price * seat.price_coefficient * 0.9


class VipPricing(PricingStrategy):
    def calculate_price(self, base_price, seat):
        return base_price * seat.price_coefficient * 1.5
