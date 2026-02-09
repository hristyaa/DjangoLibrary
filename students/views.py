from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, View
from students.models import Student, MyModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from students.forms import StudentForm

from django.core.cache import cache

from .services import StudentService


class StusentDetailView(DetailView):
    model = Student
    template_name = "students/students_detail.html"
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student_id = self.object.id

        context["full_name"] = StudentService.get_full_name(student_id)
        context["average_grade"] = StudentService.calculate_average_grade(student_id)
        context["has_passed"] = StudentService.has_passed(student_id)

        return context


def my_view(request):
    # Попытка получить данные из кеша
    data = cache.get("my_key")

    # Если данные не найдены в кеше, выполняем вычисления и сохраняем результат в кеш
    if not data:
        data = "some expensive computation"
        cache.set("my_key", data, 60 * 15)  # Кешируем данные на 15 минут

    # Возвращаем ответ с данными
    return HttpResponse(data)


def next_year(year: str) -> str:
    mapping = {
        Student.FIRST_YEAR: Student.SECOND_YEAR,
        Student.SECOND_YEAR: Student.THIRD_YEAR,
        Student.THIRD_YEAR: Student.FOURTH_YEAR,
        Student.FOURTH_YEAR: Student.FOURTH_YEAR,  # дальше не повышаем
    }
    return mapping.get(year, Student.FOURTH_YEAR)


class PromoteStudentView(LoginRequiredMixin, View):
    def post(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)

        if not request.user.has_perm("students.can_promote_student"):
            return HttpResponseForbidden("У вас нет прав для перевода студента.")

        student.year = next_year(student.year)
        student.save()

        return redirect("students:student_list")


class ExpelStudentView(LoginRequiredMixin, View):
    def post(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)

        if not request.user.has_perm("students.can_expel_student"):
            return HttpResponseForbidden("У вас нет прав для исключения студента.")

        student.delete()

        return redirect("students:student_list")


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        if not self.request.user.has_perm("students.view_student"):
            return Student.objects.none()
        return Student.objects.all()


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student_list")


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("students:student_list")


class MyModelCreateView(CreateView):
    model = MyModel
    fields = ["name", "description"]
    template_name = "students/mymodel_form.html"
    success_url = reverse_lazy("students:mymodel_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.context_data["error_message"] = "Please correct the errors"
        return response


class MyModelListView(ListView):
    model = MyModel
    template_name = "students/mymodel_list.html"
    context_object_name = "mymodels"

    def get_queryset(self):
        # queryset = super().get_queryset().filter(is_active=True)
        return MyModel.objects.filter(is_active=True)


class MyModelDetailView(UpdateView):
    model = MyModel
    template_name = "students/mymodel_detail.html"


class MyModelUpdateView(UpdateView):
    model = MyModel
    fields = ["name", "description"]
    template_name = "students/mymodel_form.html"
    success_url = reverse_lazy("students:mymodel_list")


class MyModelDeleteView(DeleteView):
    model = MyModel
    template_name = "students/mymodel_confirm_delete.html"
    success_url = reverse_lazy("students:mymodel_list")


# Create your views here.Пример
# def example_view(request):
#     return render(request, 'app/example.html')
#
#
# def show_data(request):
#     if request.method == 'GET':
#         return render(request, 'app/show_data.html')
#
#
# def submit_data(request):
#     request.GET
#     request.POST
#     if request.method == 'POST':
#         return HttpResponse('Данные отправлены')
#
#
# def show_item(request, item_id):
#      return render(request, 'app/item.html', {'item_id': item_id})


def about(request):
    return render(request, "students/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        message = request.POST.get("message")

        return HttpResponse(f'Спасибо, {name}!Сообщение: "{message}" получено.')
    return render(request, "students/contact.html")


def example_view(request):
    return render(request, "students/example_view.html")


def index(request):
    student = Student.objects.get(id=1)
    context = {
        "student_name": f"{student.first_name} {student.last_name}",
        "student_year": student.get_year_display(),
    }
    return render(request, "students/index.html", context=context)


def student_detail(request, student_id):
    student = Student.objects.get(id=student_id)
    context = {
        "student": student,
    }
    return render(request, "students/student_detail.html", context=context)


def student_list(request):
    students = Student.objects.all()
    context = {
        "students": students,
    }

    return render(request, "students/student_list.html", context=context)
