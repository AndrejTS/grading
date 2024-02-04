import random

from django.core.management.base import BaseCommand

from grading.models import Student, Grade


class Command(BaseCommand):
    help = "Add random grades"

    def handle(self, *args, **options):
        students = Student.objects.prefetch_related("subjects")

        bulk_list = list()
        for student in students:
            for subject in student.subjects.all():
                mean = random.uniform(1, 5)
                variance = random.randint(0, 4)
                low = round(mean - variance if (mean - variance) >= 1 else 1)
                high = round(mean + variance if (mean + variance) <= 5 else 5)

                for _ in range(random.randint(3, 10)):
                    grade = random.randint(low, high)
                    bulk_list.append(
                        Grade(grade=grade, subject=subject, student=student)
                    )

        Grade.objects.bulk_create(bulk_list)
