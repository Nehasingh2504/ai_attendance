from django.db import models

# Define dynamic fields
fields = {
    "name": models.CharField(max_length=20),
    "__module__": __name__,  # Important: tells Django the model belongs to this module
}

# Add 31 date columns using a loop
for i in range(1, 32):
    fields[f"{i}"] = models.CharField(max_length=1)

# Create model dynamically
MyModel = type("attendance", (models.Model,), fields) #type(class_name, bases, attributes)

'''
MyModel = type(
    "attendance",           # class name (string)
    (models.Model,),     # base classes (tuple) → inherit from Django's models.Model
    fields               # dictionary of attributes (fields we created in a loop)
)
'''
    
class student(models.Model):
    Name = models.CharField(max_length=20)
    Photo = models.ImageField(null=True,blank=True,upload_to="images/")
    Class = models.IntegerField(default=1)