# Generated by Django 4.1.7 on 2023-02-27 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_element_include'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='element',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Елемент', 'verbose_name_plural': 'Елементы'},
        ),
        migrations.AlterModelOptions(
            name='elementinelement',
            options={'ordering': ['to_elem__name'], 'verbose_name': 'Елементы в элементе', 'verbose_name_plural': 'Елементы в элементах'},
        ),
        migrations.AlterField(
            model_name='element',
            name='measurement_value',
            field=models.CharField(blank=True, help_text='В каких единицах запишем количество', max_length=50, null=True, verbose_name='Единица измерения'),
        ),
    ]
