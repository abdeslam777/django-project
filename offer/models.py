from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Offer(models.Model):
    title= models.CharField(max_length=200)
    description=models.TextField()
    # supervisor = models.ForeignKey(User, on_delete=models.CASCADE)
    supervisor =models.CharField(max_length=50)
    skills_required = models.TextField(help_text="The skills required for the project.")
    duration = models.PositiveIntegerField(help_text="The duration of the project in months.")
    is_active = models.BooleanField(default=True, help_text="Whether the project offer is active or closed.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date the offer was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The last update date of the offer.")
    
    def __str__(self):
        return self.title
    
# User.add_to_class('watchlist', models.ManyToManyField(Offer, blank=True))
    
class OfferApplication(models.Model):
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} - {self.offer.title}'


# class Watchlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_watchlist')
#     offer = models.ForeignKey('Offer', on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Watchlist: {self.user.username} -> {self.offer.title}"

# class Application(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('rejected', 'Rejected'),
#     ]

#     student = models.ForeignKey(User, on_delete=models.CASCADE)  # The student is a User
#     offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     date_applied = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Application for {self.offer.title} by {self.student.username}"