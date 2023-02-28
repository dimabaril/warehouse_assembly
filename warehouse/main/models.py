from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Element(models.Model):
    """Element model."""
    name = models.CharField(
        max_length=50,
        verbose_name="Название",
        help_text="Название позиции",
        null=True,
        blank=True,
    )
    measurement_value = models.CharField(
        max_length=50,
        verbose_name="Единица измерения",
        help_text="В каких единицах запишем количество",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Описание позиции",
        null=True,
        blank=True,
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name="Автор",
        null=True,
    )
    include = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        null=True,
        through='ElementInElement',
        related_name='elementinelements'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Елемент"
        verbose_name_plural = "Елементы"

    def __str__(self):
        if self.name:
            return self.name[:15]
        return super().__str__()


class ElementInElement(models.Model):
    """Some text."""
    from_elem = models.ForeignKey(
        Element,
        related_name='from_elems',
        on_delete=models.CASCADE,
    )
    to_elem = models.ForeignKey(
        Element,
        related_name='to_elems',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        blank=True,
        null=True,
    )
    # pub_date = models.DateTimeField(
    #     auto_now_add=True,
    #     verbose_name="Дата публикации",
    # )

    class Meta:
        ordering = ['to_elem__name']
        verbose_name = "Елементы в элементе"
        verbose_name_plural = "Елементы в элементах"
        constraints = [
            models.UniqueConstraint(fields=['from_elem', 'to_elem'],
                                    name='unique element in element')
        ]

    # def __str__(self):
    #     if self.amount:
    #         return str(self.amount[:15])
    #     return super().__str__()


# Все входящие с id=1 Element.objects.filter(to_elems__from_elem_id=1)
# Все куда входит с id=1 Element.objects.filter(from_elems__to_elem=3)
# ElementInElement.objects.update_or_create(from_elem_id=1,to_elem_id=2,amount=20)
# ElementInElement.objects.get(from_elem_id=1,to_elem_id=2).delete()

# from main.models import Element
# from main.models import ElementInelement
