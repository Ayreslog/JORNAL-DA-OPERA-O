from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Issue(models.Model):
    week_number = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200, default='Jornal da Operação')
    pdf = models.FileField(upload_to='pdf/')
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"semana-{self.week_number}-{self.start_date}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('issue_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"Semana {self.week_number} - {self.start_date} a {self.end_date}"

class PageImage(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='pages')
    image = models.ImageField(upload_to='pages/%Y/%m/%d/')
    page_number = models.PositiveIntegerField()

    class Meta:
        ordering = ['page_number']
        unique_together = ('issue', 'page_number')

    def __str__(self):
        return f"{self.issue} – Página {self.page_number}"