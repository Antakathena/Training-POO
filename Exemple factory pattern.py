class Factory():
    def make(self):
        raise NotImplementedError

class PizzaFactory(Factory):
    def __init__(self, pate, sauce_tomate):
        self.pate = pate
        self.sauce_tomate = sauce_tomate

    def make(self, garniture=tuple()):
        # on personnalise ici la garniture, notamment en ajoutant de la mozarella et du basilic
        return Pizza(self.pate, self.sauce_tomate, ["mozzarella", "basilic", *garniture])


class Pizza:
    def __init__(self, pate, sauce_tomate, garniture):
        self.pate = pate
        self.sauce_tomate = sauce_tomate
        if "ananas" in garniture:
            raise NotImplementedError
        self.garniture = garniture

    def __str__(self):
        return f"Une belle pizza avec {self.sauce_tomate}, une pâte {self.pate}. Garniture : {self.pate}." + ", ".join(str(g) for g in self.garniture)


pizza_factory = PizzaFactory(pate="épaisse", sauce_tomate="crème fraiche")

# ... plus loin dans le code ..

margherita = pizza_factory.make()
print("margherita:", margherita)
# margherita: Une belle pizza avec crème fraiche, une pâte épaisse. Garniture : épaisse.mozzarella, basilic
reine = pizza_factory.make(["jambon", "champignon"])
print("reine:", reine)
# reine: Une belle pizza avec crème fraiche, une pâte épaisse. Garniture : épaisse.mozzarella, basilic, jambon, champignon
hawaienne = pizza_factory.make(["ananas", "tabasco"])
# Traceback (most recent call last):
#   File "<string>", line 35, in <module>
# File "<string>", line 12, in make
#   File "<string>", line 20, in __init__
# NotImplementedError0
