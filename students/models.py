from django.db import models


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"
        ordering = [
            "name",
        ]


class Student(models.Model):
    # first_name = models.CharField(max_length=150, verbose_name='Имя')
    # last_name = models.CharField(max_length=150, verbose_name='Фамилия', unique=True)
    #
    # age = models.IntegerField(help_text='Введите возраст студента')
    # is_active = models.BooleanField(default=True)
    # description = models.TextField(null=True, blank=True)
    # created_at = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to='photos/', verbose_name='Фотография')
    # group = models.ForeignKey(Group, on_delete=models.SET, related_name='students')
    # profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag)
    #
    # STATUS_CHOICES = [
    #     ('draft', 'Draft'),
    #     ('published', 'Published'),
    # ]
    #
    # status = models.CASCADE(max_leght=10, choices=STATUS_CHOICES, default='draft')
    #
    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'
    #
    # class Meta:
    #     verbose_name = 'студент'
    #     verbose_name_plural = 'студенты'
    #     ordering = ['last_name']
    #     db_table = 'custom_table_name'

    FIRST_YEAR = "first-year"
    SECOND_YEAR = "second-year"
    THIRD_YEAR = "third-year"
    FOURTH_YEAR = "fourth-year"

    YEAR_IN_SCHOOL_CHOICES = [
        (FIRST_YEAR, " Первый курс"),
        (SECOND_YEAR, "Второй курс"),
        (THIRD_YEAR, "Третий курс"),
        (FOURTH_YEAR, "Четвертый курс"),
    ]

    first_name = models.CharField(max_length=10, verbose_name="Имя")
    last_name = models.CharField(max_length=10, verbose_name="Фамилия")
    email = models.EmailField()
    year = models.CharField(
        max_length=11,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FIRST_YEAR,
        verbose_name="Курс",
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="students", null=True, blank=True
    )
    enrollment_date = models.DateField()
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "студент"
        verbose_name_plural = "студенты"
        ordering = [
            "last_name",
        ]
        permissions = [
            ("can_promote_student", "Can promote student"),
            ("can_expel_student", "Can expel student"),
        ]


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.FloatField

    def __str__(self):
        return f"{self.subject}: {self.score}"
