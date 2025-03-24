from django.core.exceptions import ValidationError
from django.db import models

from authentication.models import User


class CategoryQuerySet(models.QuerySet):

    def top_level(self):
        """Returns only top-level categories (no parent)."""
        return self.filter(parent__isnull=True)

    def with_parent(self):
        """Preloads parent categories to reduce queries."""
        return self.select_related("parent")

    def with_children(self):
        """Preloads child categories using Prefetch."""
        return self.prefetch_related("subcategories")

    def get_subcategories(self, parent_category):
        """Returns direct children of a given category."""
        return self.filter(parent=parent_category)


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_category_tree(self):
        return self.get_queryset().with_parent().with_children()


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def clean(self):
        """Ensure a category cannot be its own parent."""
        if self.parent == self:
            raise ValidationError("A category cannot be its own parent.")

    def save(self, *args, **kwargs):
        """Call clean() before saving to enforce validation."""
        self.clean()
        super().save(*args, **kwargs)

    def is_top_level(self):
        """Checks if this is a top-level category."""
        return self.parent is None


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    is_approved = models.BooleanField(default=False)
