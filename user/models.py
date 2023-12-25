from django.core.validators import MinValueValidator
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings

PRIORITY_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)


class AbstractModel(models.Model):
    updated_date = models.DateTimeField(
        blank=True,
        auto_now=True,
        verbose_name='Updated Date',
        help_text='',
    )
    created_date = models.DateTimeField(
        blank=True,
        auto_now_add=True,
        verbose_name='Created Date',
        help_text='',
    )

    class Meta:
        abstract = True


class Task(AbstractModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
        help_text='',
    )
    description = models.CharField(
        default='',
        max_length=254,
        blank=False,
        verbose_name='Description',
        help_text='',
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        verbose_name='Due Date',
        help_text='',
    )

    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='medium',
    )
    done = models.BooleanField(
        default=False,
        verbose_name='Done',
        help_text='',
    )

    def change_done_status(self):
        if self.done:
            self.done = False
        else:
            self.done = True

    def name(self):
        return f"{self.user}"

    def __str__(self):
        return f'Task Setting: {self.description}'

    class Meta:
        verbose_name = 'Task Setting'
        verbose_name_plural = 'Task Settings'
        ordering = ('-created_date',)
