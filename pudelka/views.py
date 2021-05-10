from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from pudelka.models import Porownywarka, Firma
from django.views import View

class Calculator(View):
    def get(self, request):
        weight=''
        height=''
        age=''
        gender=''
        if 'gender' in request.session:
            gender = request.session['gender']
        if 'weight' in request.session:
            weight = request.session['weight']
        if 'height' in request.session:
            height = request.session['height']
        if 'age' in request.session:
            age = request.session['age']
        return render(request, 'calculator.html', {'gender': gender, 'weight': weight, 'height': height, 'age': age})

    def post(self, request):
        gender = request.POST.get('gender')
        age = request.POST.get('age', 0)
        weight = request.POST.get('weight', 0)
        height = request.POST.get('height', 0)
        activity= request.POST.get('activity')
        diet = request.POST.get('diet')
        if weight and height and age:
            request.session['gender'] = gender
            request.session['weight'] = int(weight)
            request.session['height'] = int(height)
            request.session['age'] = int(age)
            bmrcal1 = Children(gender, age)
            bmical = BMI(weight, height)
            bmrcal = BMR(gender, activity, weight, height, age)

            if gender != "Child":
                result = Calc(gender, activity, weight, height, age, diet)

            if gender == "Child":
                result = Porownywarka.objects.filter(dieta='Junior')

          #  for firma in result:
            #    print(firma.firma for reservation in firma.Porownywarka_set.all())

        else:
            error= 'Prosze uzupelnic info!'
            return render(request, 'calculator.html', {'error': error})
        return render(request, 'calculator.html', {'bmical': bmical, 'bmrcal':round(bmrcal,0), 'bmrcal1':bmrcal1,'result': result})

class Mommy(View):
    def get(self, request):
        weight = ''
        height = ''
        age = ''
        pregnat=''
        if 'weight' in request.session:
            weight = request.session['weight']
        if 'height' in request.session:
            height = request.session['height']
        if 'age' in request.session:
            age = request.session['age']
        if 'pregnat' in request.session:
            pregnat = request.session['pregnat']
        return render(request, 'mommy.html', {'weight': weight, 'height': height, 'age': age, 'pregnat': pregnat})

    def post(self, request):
        weight = request.POST.get('weight', 0)
        height = request.POST.get('height', 0)
        age = request.POST.get('age', 0)
        activity = request.POST.get('activity')
        pregnat = request.POST.get('pregnat')
        print(pregnat)
        if weight and height and age:
            bmrcal= BMR("Woman", activity, weight, height, age)
            print(bmrcal, 'bmrcal')
            if pregnat== '2trym':
                bmrcal=  bmrcal+ 360
                print(bmrcal)
            if pregnat== '3trym':
                bmrcal = bmrcal + 475
            if pregnat == 'breast':
                bmrcal = bmrcal + 670
            result = Porownywarka.objects.filter(dieta='Fit Mammy')
            result = result.filter(kalorycznosc__gt=(bmrcal-200), kalorycznosc__lte=(bmrcal+200))

            request.session['weight'] = int(weight)
            request.session['height'] = int(height)
            request.session['age'] = int(age)
            request.session['pregnat'] = pregnat

        else:
            error= 'Prosze uzupelnic info!'
            return render(request, 'calculator.html', {'error': error})
        return render(request, 'mommy.html', {'bmrcal':round(bmrcal,0), 'result': result})

def Children(gender, age):
    if gender == "Child":
        if int(age) >1 and int(age) <=3:
            bmrcal = 1000
        if int(age) >3 and int(age) <=6:
            bmrcal= 1400
        if int(age) >6 and int(age) <=9:
            bmrcal= 1800
        return bmrcal

def Calc(gender, activity, weight, height, age, diet=''):
    bmrcal = BMR(gender, activity, weight, height, age)
    result = Porownywarka.objects.filter(kalorycznosc__gt=(bmrcal-200), kalorycznosc__lte=(bmrcal+200))
    if not result:
        print('ok')
        result = Porownywarka.objects.filter(kalorycznosc__gt=(bmrcal-300), kalorycznosc__lte=(bmrcal+300))
    if gender== "Man":
        result = result.exclude(dieta='Fit Mammy')
    if diet != '':
        if diet == "Diabetic":
            result = result.filter(dieta='Diabetic')
        if diet == "LactoseFree":
            result = result.filter(dieta='Lactose Free')
        if diet == "GlutenFree":
            result = result.filter(dieta='Gluten Free')
        if diet == "LactoseGlutenFree":
            result = result.filter(dieta='Lactose & Gluten Free')
        if diet == "VegeFish":
            result = result.filter(dieta='Vege + Fish').filter(dieta='Vege+Fish')
        if diet == "Vege":
            result = result.filter(dieta='Vege')
        if diet == "Wegan":
            result = result.filter(dieta='Wegan')
        if diet == "LessCarb":
            result = result.filter(dieta='Less Carb')
        if diet == "Hashimoto":
            result = result.filter(dieta='Hypo Hashimoto')
    return result

def CatDiets(diet):
    if diet == "Diabetic":
        result = Porownywarka.objects.filter(dieta='Diabetic')
    if diet == "LactoseFree":
        result = Porownywarka.objects.filter(dieta='Lactose Free')
    if diet == "GlutenFree":
        result = Porownywarka.objects.filter(dieta='Gluten Free')
    if diet == "LactoseGlutenFree":
        result = Porownywarka.objects.filter(dieta='Lactose & Gluten Free')
    if diet == "VegeFish":
        result = Porownywarka.objects.filter(dieta='Vege + Fish').filter(dieta='Vege+Fish')
    if diet == "Vege":
        result = Porownywarka.objects.filter(dieta='Vege')
    if diet == "Wegan":
        result = Porownywarka.objects.filter(dieta='Wegan')
    if diet == "LessCarb":
        result = Porownywarka.objects.filter(dieta='Less Carb')
    if diet == "Hashimoto":
        result = Porownywarka.objects.filter(dieta='Hypo Hashimoto')
    return result

def BMI(weight, height):
    BMI = float(weight) / ((float(height)/100) * (float(height)/100))
    if BMI < 18.5:
        BMIcalc = 'Underweight'
    if BMI > 18.5 and BMI < 24.9:
        BMIcalc = 'Normal weight'
    if BMI > 25 and BMI < 29.9:
        BMIcalc = 'Overweight'
    if BMI > 30:
        BMIcalc = 'Obesity'
    return BMIcalc

def BMR(gender, activity, weight, height, age):
    cal=0
    BMR=0
    if gender == 'Woman' or gender == 'Pregnat':
        BMR = 655.1 + (9.567 * float(weight)) + (1.85 * float(height)) - (4.68 * float(age))
    if gender == 'Man':
        BMR = 66.47 + (13.7 * float(weight)) + (5 * float(height)) - (6.76 * float(age))
    if activity == '1time':
        cal = 1.2 * BMR
    if activity == '2time':
        cal = 1.3755 * BMR
    if activity == '3time':
        cal = 1.4654 * BMR
    if activity == '4time':
        cal = 1.55 * BMR
    if activity == '5time':
        cal = 1.725 * BMR
    if activity == '6time':
        cal = 1.9 * BMR
    return cal

class BoxList(View):
    def get(self, request):
        result= Porownywarka.objects.all()
        return render(request, 'box_list.html', {'result': result})

class DietChoices(View):
    def get(self, request):
        return render(request, 'diet-choices.html')
    def post(self, request):
        calories =request.POST.get('calories', 0)
        print(calories)
        result = Porownywarka.objects.filter(kalorycznosc=int(calories))
        return render(request, 'diet-choices.html', {'result': result})

class Choices(View):
    def get(self, request):
        return render(request, 'choices.html')
    def post(self, request):
        return render(request, 'choices.html')