
products = {}
length = len(products)


class Product:
    def __init__(self):
        self.products = products
        self.length = length

    def add(self, name, cost, amount):
        item = self.exist(name)
        if self.exist(name):
            item['amount'] += amount
            return self
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
        return self

    def get(self, id):
        if not self.products.get(id):
            return False
        product = self.products[id]
        return {
            'id': id,
            'name': product['name'],
            'cost': product['cost'],
            'amount': product['amount']
        }

    def exist(self, name):
        for id in self.products:
            product = self.products[id]
            if product['name'] == name:
                return product

    def sale(self, id, amount):
        if not self.products:
            return False
        if not self.products[id]:
            return False
        item = self.products[id]

        item['amount'] = amount
        self.update(id, item)
        return True

    def get_all(self):
        return self.products

    def update(self, id, data):
        if id:
            self.products[id].update(data)
            return True

    def delete(self, id):
        if id:
            self.products.pop(id)
            return True
