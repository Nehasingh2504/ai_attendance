from django.db import models
import os

# Define fields dictionary
fields = {
    "name": models.CharField(max_length=20),
    "__module__": __name__,   # IMPORTANT: so Django knows this model belongs to your app
}

# Add day_1 ... day_31
for i in range(1, 32):
    fields[f"day_{i}"] = models.CharField(max_length=1, blank=True, null=True)

# Create model dynamically
Attendance = type("Attendance", (models.Model,), fields)

'''
MyModel = type(
    "attendance",           # class name (string)
    (models.Model,),     # base classes (tuple) → inherit from Django's models.Model
    fields               # dictionary of attributes (fields we created in a loop)
)
'''
def student_image_path(instance, filename):
    return os.path.join("student", f"class_{instance.Class}", filename)

class student(models.Model):
    Name = models.CharField(max_length=20)
    Photo = models.ImageField(null=True,blank=True,upload_to=student_image_path)
    Class = models.IntegerField(default=1)