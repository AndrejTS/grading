"""
This script and files to upload must be in root directory of project (on same level as manage.py) 
Usage: 
1. run django shell -> python manage.py shell
2. import this script > import upload_users
3. run it -> upload_users.run()
"""


import csv

from grading.models import User, Teacher, Student, Subject


def run():
    with open("ucitele.tsv") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            subjects = []
            for sub_code in row["PREDMETY"].split(","):
                sub, _ = Subject.objects.update_or_create(code=sub_code, defaults={})
                subjects.append(sub)

            try:
                u = User.objects.get(username=row["LOGIN"])
            except User.DoesNotExist:
                u = User.objects.create_user(
                    username=row["LOGIN"], password=row["HESLO"]
                )
                u.is_teacher = True
                u.first_name = row["JMENO"]
                u.last_name = row["PRIJMENI"]
                u.save()
                Teacher.objects.create(user=u)

            u.teacher.subjects.add(*subjects)

            print(f'Added teacher with login: {row["LOGIN"]}')

    with open("studenti.tsv") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            subjects = []
            for sub_code in row["PREDMETY"].split(","):
                sub, _ = Subject.objects.update_or_create(code=sub_code, defaults={})
                subjects.append(sub)

            try:
                u = User.objects.get(username=row["LOGIN"])
            except User.DoesNotExist:
                u = User.objects.create_user(
                    username=row["LOGIN"], password=row["HESLO"]
                )
                u.is_student = True
                u.save()
                Student.objects.create(user=u)

            u.student.subjects.add(*subjects)

            print(f'Added student with login: {row["LOGIN"]}')
