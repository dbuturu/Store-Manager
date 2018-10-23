from .product import Product

product = Product()

sales = {}
length = 0

class Sale:
    def __init__(self):
        self.sales = sales
        self.length = length
        self.id = 0
        self.product_id = 0
        self.name = ''
        self.cost = 0

    def add(self, product_id, name, cost, amount):
        if not product.sale(product_id, amount):
            return self
        self.length += 1
        self.id = self.length
        self.product_id = product_id
        self.name = name
        self.cost = cost * amount
        self.sales[self.id] = {
            'product_id': self.product_id,
            'name': self.name,
            'cost': self.cost
        }
        return self

    def get(self, id):
        if not self.sales.get(id):
            return False
        sale = self.sales[id]
        return {
            'product_id': sale['product_id'],
            'name': sale['name'],
            'cost': sale['cost']
        }

    def get_all(self):
        return self.sales

    def update(self, id, data):
        if id:
            self.sales[id].update(data)
            return True

    def delete(self, id):
        if id:
            self.sales.pop(id)
            return True
