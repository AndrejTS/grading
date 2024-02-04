from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import View, ListView
from django.contrib.auth import views as auth_views, logout
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from grading.models import User, Subject, Grade
from .decorators import student_required, teacher_required


class Index(View):
    def get(self, request):
        user = self.request.user
        if user.is_authenticated:
            if user.is_teacher:
                return HttpResponseRedirect(reverse("teacher"))
            elif user.is_student:
                return HttpResponseRedirect(reverse("student"))

        return HttpResponseRedirect(reverse("login"))


class LoginUserView(auth_views.LoginView):
    template_name = "grading/login.html"

    def get_success_url(self):
        if self.request.user.is_teacher:
            return reverse("teacher")
        elif self.request.user.is_student:
            return reverse("student")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


@method_decorator([login_required, student_required], name="dispatch")
class StudentOverviewView(ListView):
    context_object_name = "subjects"
    template_name = "grading/student_overview.html"

    def get_queryset(self):
        self.student = self.request.user.student
        subjects = {
            s.code: Grade.objects.filter(student=self.student, subject=s)
            for s in self.student.subjects.all()
        }
        return subjects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student"] = self.student
        return context


@method_decorator([login_required, teacher_required], name="dispatch")
class TeacherOverviewView(ListView):
    context_object_name = "subjects"
    template_name = "grading/teacher_overview.html"

    def get_queryset(self):
        self.teacher = self.request.user.teacher
        return self.teacher.subjects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teacher"] = self.teacher
        return context


@method_decorator([login_required, teacher_required], name="dispatch")
class TeacherSubjectView(View):
    def get(self, request, code):
        teacher = self.request.user.teacher
        subject = Subject.objects.get(code=code)

        students_grades = {
            student: Grade.objects.filter(student=student, subject=subject)
            for student in subject.student_set.all()
        }

        return render(
            request,
            "grading/teacher_subject.html",
            {
                "teacher": teacher,
                "subject": subject,
                "students_grades": students_grades,
            },
        )


@method_decorator([login_required, teacher_required], name="dispatch")
class CreateGradeView(View):
    def get(self, request, student, subject):
        return render(
            request, "grading/add_grade.html", {"student": student, "subject": subject}
        )

    def post(self, request):
        student = User.objects.get(username=self.request.POST["student"]).student
        subject = Subject.objects.get(pk=self.request.POST["subject"])
        grade = self.request.POST["grade"]
        teacher = self.request.user.teacher
        if subject not in teacher.subjects.all():
            return HttpResponseForbidden()
        grade = Grade.objects.create(
            grade=grade, student=student, subject=subject, teacher=teacher
        )
        return HttpResponseRedirect(
            reverse("teacher_subject", kwargs={"code": subject})
        )


@method_decorator([login_required, teacher_required], name="dispatch")
class GradeDeleteView(DeleteView):
    def post(self, request):
        pk = self.request.POST["grade_pk"]
        grade = Grade.objects.get(pk=pk)
        if grade.subject not in self.request.user.teacher.subjects.all():
            return HttpResponseForbidden()
        grade.delete()
        subject_code = self.request.POST["subject_code"]
        return HttpResponseRedirect(
            reverse("teacher_subject", kwargs={"code": subject_code})
        )
