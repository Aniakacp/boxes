# Generated by Django 2.2.19 on 2021-03-11 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Porownywarka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dieta', models.TextField()),
                ('kalorycznosc', models.IntegerField()),
                ('cena', models.DecimalField(decimal_places=2, max_digits=6)),
                ('ilosc_posilkow', models.SmallIntegerField()),
            ],
        ),
    ]