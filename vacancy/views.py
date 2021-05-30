from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404

from vacancy.models import Specialty, Company, Vacancy


def main_view(request):
    count_vacancy_speciality = {}
    for code in Specialty.objects.all():
        count_vacancy_speciality[code.code] = Vacancy.objects.filter(specialty__code=code.code).count()
    count_vacancy_company = {}
    for company_id in Company.objects.all():
        count_vacancy_company[company_id.id] = Vacancy.objects.filter(company__id=company_id.id).count()
    return render(request, 'index.html', context={
        'specialties': Specialty.objects.all(),
        'companies': Company.objects.all(),
        'count_vacancy_speciality': count_vacancy_speciality,
        'count_vacancy_company': count_vacancy_company,
    })


def vacancies_view(request):
    count_vacancy = Vacancy.objects.count()
    return render(request, 'vacancies.html', context={
        'vacancies': Vacancy.objects.all(),
        'count_vacancy': count_vacancy,
    })


def vacancies_categories_view(request, categories):
    category = get_object_or_404(Specialty, code=categories)
    vacancies = Vacancy.objects.filter(specialty__code=categories)
    count_vacancy_category = Vacancy.objects.filter(specialty__code=categories).count()
    return render(request, 'vacancies_categories.html', context={
        'category': category,
        'vacancies': vacancies,
        'count_vacancy_category': count_vacancy_category
    })


def companies_view(request, company_pk):
    company = get_object_or_404(Company, pk=company_pk)
    count_vacancy_company = {}
    for company_pk in Company.objects.all():
        count_vacancy_company[company_pk.id] = Vacancy.objects.filter(company__id=company_pk.id).count()
    title_vacancy = company.vacancies.all()[0].title
    skill_vacancy = company.vacancies.all()[0].skills
    published_vacancy = company.vacancies.all()[0].published_at
    min_salary_vacancy = company.vacancies.all()[0].salary_min
    max_salary_vacancy = company.vacancies.all()[0].salary_max
    specialty_vacancy = company.vacancies.all()[0].specialty.title
    specialty_picture_vacancy = company.vacancies.all()[0].specialty.picture

    return render(request, 'company.html', context={
        'company': company,
        'count_vacancy_company': count_vacancy_company,
        'title_vacancy': title_vacancy,
        'skill_vacancy': skill_vacancy,
        'published_vacancy': published_vacancy,
        'min_salary_vacancy': min_salary_vacancy,
        'max_salary_vacancy': max_salary_vacancy,
        'specialty_vacancy': specialty_vacancy,
        'specialty_picture_vacancy': specialty_picture_vacancy,
    })


def vacancy_view(request, vacancy_pk):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
    return render(request, 'vacancy.html', context={
        'vacancy': vacancy,
    })


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страницы не существует!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
