from django.db import models
import uuid
class Project(models.Model):
    title = models.CharField(max_length=200)
    intro = models.TextField(max_length=255,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.title
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    # class Meta: 
    #     unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value