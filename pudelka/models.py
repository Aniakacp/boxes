from django.db import models

class Firma(models.Model):
    firma=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.firma}'

class Porownywarka(models.Model):
    firma= models.ForeignKey(Firma, on_delete=models.CASCADE)
    dieta= models.TextField()
    kalorycznosc= models.IntegerField()
    cena= models.DecimalField(max_digits=6, decimal_places=2)
    ilosc_posilkow = models.SmallIntegerField()
    opis = models.TextField(blank=True)

    def __str__(self):
        return f'{self.dieta}'



