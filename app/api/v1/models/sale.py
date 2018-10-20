from app.api.v1.models.product import Product
product = Product()

class Sale:
    sales = {}
    length = 0

    def __init__(self):
        pass

    def add(self, product_id, name, cost, amount):
        # if not self.sale(product_id,amount):
        #     return self
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

    def sale(self, product_id, amount):
        item = product.get(product_id)
        print(item['amount'])

    def get(self, id):
        sale = self.sales[id]
        return {
            'product_id': sale['product_id'],
            'name': sale['name'],
            'cost': sale['cost']
        }

    def get_all(self):
        return self.sales

    def update(self, data):
        self.sales[data.id].update(data)

    def delete(self, id):
        self.sales.pop(id)
