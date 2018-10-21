class Sale:
    def __init__(self):
        self.sales = {}
        self.length = 0
        self.id = 0
        self.product_id = 0
        self.name = ''
        self.cost = 0

    def add(self, product_id, name, cost, amount):
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

    def delete(self, id):
        if id:
            self.sales.pop(id)
