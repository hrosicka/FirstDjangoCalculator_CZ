class Kalkulacka:
    """
    Třída pro provádění základních aritmetických operací.
    """
    def secti(self, cislo1, cislo2):
        return cislo1 + cislo2

    def odecti(self, cislo1, cislo2):
        return cislo1 - cislo2

    def vynasob(self, cislo1, cislo2):
        return cislo1 * cislo2

    def vydel(self, cislo1, cislo2):
        if cislo2 == 0:
            return "Nelze dělit nulou!"
        return cislo1 / cislo2