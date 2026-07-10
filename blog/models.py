from django.db import models
from django.utils.text import slugify


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    title       = models.CharField(max_length=300)
    slug        = models.SlugField(unique=True, blank=True)
    author      = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='posts')
    category    = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    thumbnail   = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt     = models.TextField(max_length=500, blank=True)
    body        = models.TextField()
    tags        = models.CharField(max_length=300, blank=True, help_text='Comma-separated tags')
    is_published= models.BooleanField(default=True)
    views       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug, n = base, 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'; n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_tags(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


class Comment(models.Model):
    post        = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user        = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)
    name        = models.CharField(max_length=100)
    email       = models.EmailField()
    body        = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name} on {self.post.title}"
