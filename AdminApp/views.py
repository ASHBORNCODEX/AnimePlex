from django.shortcuts import render , redirect
from AdminApp.models import AnimeDB , Genre
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def dashboard(request):
    Anime_Names = AnimeDB.objects.count()
    Genres = Genre.objects.count()
    return render(request , 'DashBoard.html' , {'Anime_Names' : Anime_Names ,'Genres' :Genres})

def add_anime(request):
    genres = Genre.objects.all()  # fetch all genres from DB
    return render(request, 'AddAnime.html', {'genres': genres})


def save_anime(request):
    if request.method == "POST":
        jap_name = request.POST.get('jap_name')
        eng_name = request.POST.get('eng_name')
        duration = request.POST.get('duration')
        description = request.POST.get('description')
        episode = request.POST.get('episode')
        studio = request.POST.get('studio')
        anime_type = request.POST.get('type')
        producers = request.POST.get('producer')
        image = request.FILES['anime_image']
        versions = request.POST.getlist('versions')

        # Create AnimeDB object
        obj = AnimeDB(
            Jap_Name=jap_name,
            Eng_Name=eng_name,
            Description=description,
            Episode=episode,
            Duration=duration,
            Studio=studio,
            Producer=producers,
            Image=image,
            versions = versions,
            type = anime_type
        )
        obj.save()

        # Get selected genres from form as list of IDs
        selected_genre_ids = request.POST.getlist('genres')  # 'genres' matches the <select name="genres" multiple>

        # Add genres to the anime object (assuming AnimeDB has ManyToManyField to Genre named genres)
        if selected_genre_ids:
            genres = Genre.objects.filter(id__in=selected_genre_ids)
            obj.genres.set(genres)  # set many-to-many relationship

        return redirect(add_anime)


def view_anime(request):
    anime = AnimeDB.objects.all()
    return render(request,'ViewAnime.html',{'anime':anime})

def edit_anime(request, Anime_ID):
    anime = AnimeDB.objects.get(id=Anime_ID)
    all_genres = Genre.objects.all()
    selected_genres = anime.genres.all().values_list('id', flat=True)
    selected_versions = anime.versions  # This is already a list from MultiSelectField
    selected_type = anime.type

    return render(request, 'EditAnime.html', {
        'data': anime,
        'genres': all_genres,
        'selected_genres': list(selected_genres),
        'selected_versions': selected_versions,
        'selected_type': selected_type
    })



def update_anime(request,Anime_ID):
    if request.method == "POST":
        jap_name = request.POST.get('jap_name')
        eng_name = request.POST.get('eng_name')
        duration = request.POST.get('duration')
        description = request.POST.get('description')
        episode = request.POST.get('episode')
        anime_type = request.POST.get('type')
        studio = request.POST.get('studio')
        producers = request.POST.get('producer')
        selected_genre_ids = request.POST.getlist('genres[]')  # genres from form
        versions = request.POST.getlist('versions')

        try:
            image_file = request.FILES['anime_image']
            fs = FileSystemStorage()
            file = fs.save(image_file.name, image_file)
        except MultiValueDictKeyError:
            file = AnimeDB.objects.get(id=Anime_ID).Image

        # Update main fields
        anime_obj = AnimeDB.objects.get(id=Anime_ID)
        anime_obj.Jap_Name = jap_name
        anime_obj.Eng_Name = eng_name
        anime_obj.Episode = episode
        anime_obj.Description = description
        anime_obj.Duration = duration
        anime_obj.Studio = studio
        anime_obj.type = anime_type
        anime_obj.Producer = producers
        anime_obj.Image = file
        anime_obj.versions = versions  # MultiSelectField can take a list directly
        anime_obj.save()

        # Update genres
        anime_obj = AnimeDB.objects.get(id=Anime_ID)
        if selected_genre_ids:
            genres = Genre.objects.filter(id__in=selected_genre_ids)
            anime_obj.genres.set(genres)
        else:
            anime_obj.genres.clear()
    return redirect(view_anime)



def delete_anime(request,A_ID):
    Anime = AnimeDB.objects.filter(id=A_ID)
    Anime.delete()
    return redirect(view_anime)


def admin_login_page(request):
    return render(request , 'AdminLogin.html')

def admin_login(request):
    if request.method=="POST":
        u_name = request.POST.get('username')
        pwd = request.POST.get('password')
        if User.objects.filter(username__contains=u_name).exists():
            x = authenticate(username = u_name , password = pwd)
            if x is not  None :
                login(request , x)
                request.session['username'] = u_name
                request.session['password'] = pwd
                return redirect(dashboard)
            else:
                return redirect(admin_login_page)
        else:
            return redirect(admin_login_page)






