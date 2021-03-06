# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from schema.models import Recipes, Ingredient, Meals, like_recipe, Recipes_detail, Recipes_tag, contain_tag, Recipes_HitCount, Recipes_Comment
from django.core.exceptions import *
from django.template.loader import render_to_string, get_template
from django_tables2 import RequestConfig
from django.db import connection
import django_tables2 as tables
import wikipedia
import math
from macro import macro_recommend
from hitcount.views import HitCountDetailView
from django_select2.forms import Select2MultipleWidget

class RecipesCountHitDetailView(HitCountDetailView):
    model = Recipes
    count_hit = True


class RecipeTable(tables.Table):
    class Meta:
        model =  Recipes

class IngreTable(tables.Table):
    class Meta:
        model =  Ingredient

class MealTable(tables.Table):
    class Meta:
        model =  Meals



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request, "home.html")

def login(request):
	return render(request, "login.html")

def search_page(request):
## search recipes based on name
	return render(request, "search.html")

def return_success(request):
  return render(request, "success.html")


def get_list(request):
    if request.method == 'POST':
        rname = request.POST.get('recipe_name', None)
        in_table = Ingredient.objects.filter(name = rname)
       	re_table = Recipes.objects.filter(name__icontains = rname).order_by("rating")[:10]
	if len(re_table) + len(in_table) == 0:
	        error_message = "Sorry, no recipe nor ingredient found in our database."
        	return render(request, 'error.html', {"error_message": error_message})
        return render(request, "user_recipes.html", {"in_table":in_table, "re_table":re_table, "usr":False})
    else:
        return render(request, 'search.html')

def get_list_tag(request):
    if request.method == 'POST':
        tname = request.POST.get('tag_name', None)
	try:
        	tag = Recipes_tag.objects.get(detail = tname)
    	except Recipes_tag.DoesNotExist:
		error_message = "Sorry, we are not able to find your tag in out database."
		return render(request, 'error.html', {"error_message": error_message})
        
    	con_table = contain_tag.objects.filter(t_id = tag)[:10]
    	re_table = [tag.r_id for tag in con_table]
    	in_table = []
	if len(re_table) + len(in_table) == 0:
                error_message = "Sorry, no recipe nor ingredient found in our database."
                return render(request, 'error.html', {"error_message": error_message})
    	return render(request, "user_recipes.html", {"in_table":in_table, "re_table":re_table, "usr":False})
    else:
	return render(request, "search.html")



def get_list_macro(request):
    if request.method == 'POST':
	# breakfast = 360
	# lunch = 75
	# dinner = 35
	cal = request.POST.get('cal', None)
	breakfast = request.POST.get('breakfast', None)
	lunch = request.POST.get('lunch', None)
	dinner = request.POST.get('dinner', None)

	if cal=="" or breakfast=="" or lunch == "" or dinner == "":
		error_message = "Sorry, you have to fill out all the required area."
                return render(request, 'error.html', {"error_message": error_message})
        cal = float(cal)
	breakfast = float(breakfast)
	lunch = float(lunch)
	dinner = float(dinner)
	if breakfast + lunch + dinner != 10:
                error_message = "Sorry, the sum of ratio has to be 10."
                return render(request, 'error.html', {"error_message": error_message})
	
	break_table = []
	lunch_table = []
	dinner_table = []

	macro_recommend(cal, breakfast, lunch, dinner, break_table, lunch_table, dinner_table, request)
	if len(break_table) + len(lunch_table) + len(dinner_table) == 0:
		error_message = "Sorry, no recipe matches to your input. please try another one."
                return render(request, 'error.html', {"error_message": error_message})
        return render(request, "user_macro_recipes.html", {"break_table":break_table, "lunch_table":lunch_table, "dinner_table": dinner_table, "usr":False})

    else:
        return render(request, 'search.html')


def show_ingredient(request):
    return redirect("home.html")


def show_result(request):
    if request.method != 'POST':
    	return render(request, 'home.html')
    rname = request.POST.get('check')
    id = request.POST.get('recipeID')
    id = id.replace("-", "")
    already = request.POST.get('already')
    rec = Recipes.objects.get(rid=id)
    cal = rec.calories
    pro = rec.protein
    fat = rec.fat
    sod = rec.sodium
    creator = rec.creator
    rname = rec.name
    raw_rate = rec.rating
    carb = int(math.ceil((cal - pro * 4.0 + fat * 9.0) / 4.0))
    if carb < 0:
	    carb = 0.0
    rating_display = str(raw_rate)
    rating = str(raw_rate*10) + "%"
    table = {"Calories":cal,
             "Protein":pro,
             "Fat":fat,
             "Sodium":sod,
	     "Carb": carb
    }
    result = contain_tag.objects.filter(r_id = rec)
    tags = [item.t_id.detail for item in result]
    f = like_recipe.objects.filter(user_id = request.user, r_id = rec)
##  One more hit
    r_hit, created = Recipes_HitCount.objects.get_or_create(recipe = rec)
    hit_count = r_hit.hitcount
    hit_count += 1
    r_hit.hitcount = hit_count
    r_hit.save()
    comments = Recipes_Comment.objects.order_by('up_vote').filter(recipe = rec)
    diction = {"myFavorites": False,
        "table":table,
        "name":rname,
        "rating_w":rating,
        "rating": raw_rate,
        "creator":creator,
        "recipeID": id,
        "tags" : tags,
        "rating_display" : rating_display,
        "hit_count" : hit_count,
        "comments" : comments
    }
    diction["myFavorites"] = len(f) != 0
#cursor.close()
    return render(request, "show_result.html", diction)  


def enter(request):
    return render(request, "add.html")
def ai(request):
    return render(request, "add_i.html")
def aj(request):
    tags = Recipes_tag.objects.all()
    diction = {'tags' : tags}
    return render(request, "add_r.html", diction)
def am(request):
    return render(request, "add_m.html")

def pour(request):
    if request.method == 'POST':
	username = request.user.username
        kind = request.POST.get('type')
        name = request.POST.get('name')
        desc = request.POST.get('desc', '')
        cal = request.POST.get('calorie')
        pro = request.POST.get('protein')
        fat = request.POST.get('fat')
        sod = request.POST.get('sodium')
       	if kind == "add ingredient":
       	    i = Ingredient(name = name, calories = cal,protein = pro,fat = fat,sodium = sod, creator = username)
       	    i.save()
       	if kind == "add recipe":
	    tag_id = request.POST.getlist('tag_id[]')
	    print "\n\n\nselect tag: ", tag_id, "\n\n\n"
            instructions = request.POST.get('message')
       	    r = Recipes(name = name,rating = 0,calories = cal,protein = pro,fat = fat, sodium = sod, creator = username)
       	    r.save()
            id = r.rid
            r_d = Recipes_detail(r_id = r, instructions= instructions)
            r_d.save()
	    t_table = Recipes_tag.objects.filter(id__in = tag_id)
	    for t in t_table:
		new_t = contain_tag(r_id = r, t_id = t)
	    	new_t.save()
       	if kind == "add meal":
       	    m = Meals(name = name,rating = 0, calories = cal,protein = pro,fat = fat, sodium = sod, creator = username)
       	    m.save()
       	return redirect("home.html")
    else:
        return render(request, 'add.html');


def check_recipe_ins(request):
    recipeName = request.POST.get('recipeName')
    recipeID= request.POST.get('recipeID')
    recipeID = recipeID.replace("-", "")
    try:
        detail = Recipes_detail.objects.get(r_id = recipeID)
        text = detail.instructions
	##text = text.replace('\n', '<br>')
	
    except Recipes_detail.DoesNotExist:
        text = "we don't know"
    diction = {
        'recipeName' : recipeName,
        'recipeID' : recipeID,
        'text' : text
    }
    return render(request, "recipe_instructions.html", diction)

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")
