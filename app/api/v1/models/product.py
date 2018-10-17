
class Product:
    products = {}
    length = 0

    def __init__(self):
        pass

    def add(self, name, cost, amount):
        self.length += 1
        self.id = self.length
        self.name = name
        self.cost = cost
        self.amount = amount
        self.products[self.id] = {
            'name': self.name,
            'cost': self.cost,
            'amount': self.amount
        }

    def get(self, id):
        product = self.products[id]
        return {
            'id': id,
            'name': product['name'],
            'cost': product['cost'],
            'amount': product['amount']
        }

    def get_all(self):
        return self.products

    def update(self, data):
        self.products[data.id].update(data)

    def delete(self, id):
        self.products.pop(id)
