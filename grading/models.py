from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="teacher"
    )
    subjects = models.ManyToManyField("Subject", blank=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="student"
    )
    subjects = models.ManyToManyField("Subject", blank=True)

    def __str__(self):
        return self.user.username


class Grade(models.Model):
    GRADE_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    grade = models.SmallIntegerField(
        choices=GRADE_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="grades"
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name="grades"
    )


class Subject(models.Model):
    code = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.code
