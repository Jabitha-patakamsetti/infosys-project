from django.db import models

class TrainingRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'),
                 ('Approved', 'Approved'),
                 ('Rejected', 'Rejected')],
        default='Pending'
    )
    account_manager = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Manager'}
    )
    course_duration = models.PositiveIntegerField(help_text="Duration in days")  # New field
    employee_count = models.PositiveIntegerField(help_text="Number of employees involved")  # New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    






class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        limit_choices_to={'role__role_name': 'Admin'}
    )
    resource_link = models.URLField(max_length=1024, null=True, blank=True)  # For URLs (e.g., YouTube)
    created_at = models.DateTimeField(auto_now_add=True)
    employees = models.ManyToManyField(
        'authentication.User',
        related_name='enrolled_courses',
        limit_choices_to={'role__role_name': 'Employee'},
        blank=True  # Optional field
    )

    def number_of_modules(self):
        # Count the number of related modules
        return self.modules.count()

    def __str__(self):
        return self.title


class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course,
        related_name='modules',  # Links modules to a course
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    
    # General resource link (could be a URL or file)
    youtube_link = models.URLField(max_length=1024, null=True, blank=True)  # For URLs (e.g., YouTube)
    file_upload = models.FileField(upload_to='module_resources/', null=True, blank=True)  # For file uploads
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    



# Progress Model
class Progress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # ForeignKey to Course
    employee = models.ForeignKey('authentication.User', on_delete=models.CASCADE)  # ForeignKey to User
    progress_percent = models.IntegerField(default=0)

    def __str__(self):
        return f"Progress ID: {self.progress_id}, Course: {self.course}, Employee: {self.employee}"

# Feedback Model
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)  # ForeignKey to Course
    employee = models.ForeignKey('authentication.User', on_delete=models.CASCADE)  # ForeignKey to User
    rating = models.IntegerField()  # IntegerField for ratings
    comments = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name='rating_between_1_and_5')
        ]

    def __str__(self):
        return f"Feedback ID: {self.feedback_id}, Course: {self.course}, Rating: {self.rating}"
