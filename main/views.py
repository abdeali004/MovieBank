from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from main.models import UserInfo
from modules.MoviesFilter import extractMovie, imdbMovieDetail,recommendation,  googleScrap, scrapping

# Create your views here.


def home(request):
    if request.user.is_anonymous:
        return redirect("/login")
    # print(request.user)
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        user1 = User.objects.filter(username=request.POST.get(
            "username"))
        user2 = User.objects.filter(email=request.POST.get(
            "email"))
        if len(user1) == 0 and len(user2) == 0:
            user = User.objects.create_user(username=request.POST.get(
                "username"), password=request.POST.get("password"))
            user.first_name = request.POST.get("fullname")
            user.email = request.POST.get("email")
            user.is_superuser = False
            user.save()
            messages.info(
                request, 'You are registered successfully. Please Login to continue.')
            return render(request, "login.html")
        else:
            messages.warning(
                request, 'Username or E-Mail already taken. Please Sign Up using another username.')
            return render(request, "login.html")
        return render(request, "login.html")
    elif not request.user.is_anonymous:
        return redirect("/home")
    else:
        return render(request, "login.html")
    return render(request, "UserChoice.html")


def loginUser(request):
    if request.method == "POST":
        name = request.POST.get(
            "username")
        user = authenticate(
            username=name, password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            userchoice = UserInfo.objects.filter(username=name)
            if len(userchoice):
                return redirect("/home")
            else:
                return render(request, "UserChoice.html")
        else:
            # No backend authenticated the credentials
            messages.warning(
                request, 'Wrong Username or Password.')
            return render(request, "login.html")
    elif not request.user.is_anonymous:
        return redirect("/home")
    else:
        return render(request, "login.html")


def logoutUser(request):
    logout(request)
    messages.info(
        request, 'You Logout Successfully. Come back soon.')
    return redirect("/login")


def UserChoice(request):
    return render(request, "UserChoice.html")


def UserData(request):
    if request.method == "POST":
        username = request.user
        gender = request.POST.get("genderValues")
        age = request.POST.get("ageValues")
        movieType = request.POST.get("typeValues")
        lang = request.POST.get("langValues")
        genre = request.POST.get("genreValues")

        userD = UserInfo(username=username, gender=gender, age=age,
                         movieType=movieType, lang=lang, genre=genre, newUser=False, dateJoined=datetime.today())
        userD.save()
        return redirect("/home")


def movieMain(request):
    movieScrap = scrapping(recommendation())
    context = {
        "movies" : movieScrap,
    }
    return render(request, "movies.html",context)


def movieSearch(request):
    if request.method == "POST":
        result1 = False
        result2 = False
        movieG = ""
        movieTitle = request.POST.get("title").strip()
        if movieTitle:
            movies = extractMovie(movieTitle)
            if movies:
                result1 = False
            else:
                movieG = googleScrap(movieTitle)
                result1 = True
                if movieG != "":
                    result2 = True
            context = {
                "result1": result1,
                "result2": result2,
                "movieG": movieG,
                "moviesData": movies,
            }
            return render(request, "searchMovie.html", context)
    return render(request, "searchMovie.html")


def movieDetail(request, imdbId):
    data = imdbMovieDetail(imdbId)
    context = {
        "imdbId": imdbId,
        "posterBlock": data[0],
        "infoBlock": data[1],
        "ratingBlock": data[2],
        "cast": data[3],
        "review": data[4],
        "series": data[5],
    }
    return render(request, "movieDetail.html", context)
