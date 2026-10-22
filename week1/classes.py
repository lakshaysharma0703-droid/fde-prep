from dataclasses import dataclass

@dataclass
class LineItem:
    description: str
    qty: int
    unit_price: float

    @property
    def amount(self) -> float:
        return self.qty * self.unit_price

class Invoice:
    def __init__(self, vendor: str, gst_rate: float = 0.18, discount_percent: float = 0):
        if  not 0 <= discount_percent <= 100:
            raise ValueError(f"Discount must be 0-100 but got {discount_percent}")
        self.vendor = vendor
        self.gst_rate = gst_rate
        self.discount_percent = discount_percent
        self.items: list[LineItem] = []

    def add_item(self, description: str, qty: int, unit_price:float) -> None:
        self.items.append(LineItem(description,qty,unit_price))

    @property
    def subtotal(self) -> float:
        return sum(item.amount for item in self.items)

    @property
    def discount_amount(self) -> float:
        return round(self.subtotal * self.discount_percent / 100,2)

    @property
    def taxable_value(self) -> float:
        return self.subtotal - self.discount_amount

    @property
    def gst_amount(self) -> float:
        return round(self.taxable_value * self.gst_rate,2)

    def total_with_gst(self) -> float:
        return round(self.taxable_value + self.gst_amount, 2)

    def __str__(self) -> str:
        return f"Invoice from {self.vendor}: {len(self.items)} items, total RS{self.total_with_gst()}"

def print_breakdown(inv: Invoice) -> None:
    print(inv)
    print(f"  Subtotal:      ₹{inv.subtotal}")
    print(f"  Discount ({inv.discount_percent}%): -₹{inv.discount_amount}")
    print(f"  Taxable value: ₹{inv.taxable_value}")
    print(f"  GST ({inv.gst_rate:.0%}):     ₹{inv.gst_amount}")
    print(f"  Total:         ₹{inv.total_with_gst()}\n")


invoice = Invoice("Acme Suppliers")
invoice.add_item("Laptop stand", 2, 1500)
invoice.add_item("USB-C cable", 3, 299)
print_breakdown(invoice)

discounted = Invoice("Acme Suppliers", discount_percent=10)   
discounted.add_item("Laptop stand", 2, 1500)
discounted.add_item("USB-C cable", 3, 299)
print_breakdown(discounted)

try:
    Invoice("Bad Vendor", discount_percent=150)
except ValueError as e:                                      
    print(f"Rejected: {e}")