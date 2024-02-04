from django.urls import path

from grading import views


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("login/", views.LoginUserView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("student/", views.StudentOverviewView.as_view(), name="student"),
    path("teacher/", views.TeacherOverviewView.as_view(), name="teacher"),
    path(
        "teacher/<str:code>/",
        views.TeacherSubjectView.as_view(),
        name="teacher_subject",
    ),
    path(
        "add_grade/<str:student>/<str:subject>/",
        views.CreateGradeView.as_view(),
        name="add_grade",
    ),
    path("add_grade/", views.CreateGradeView.as_view(), name="add_grade"),
    path("delete_grade/", views.GradeDeleteView.as_view(), name="delete_grade"),
]
