from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from AdminApp.models import AnimeDB, Genre, CommentDB, RatingDB
from WebApp.models import RegistrationDB , WatchListDB
from .forms import CommentForm, RatingForm
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce



def homepage(request):
    # Top-rated anime (sorted by average rating)
    rating = AnimeDB.objects.annotate(avg_rating=Coalesce(
            Avg('ratings__value'),  # must match related_name
            Value(0.0),
            output_field=FloatField()
        )
    ).order_by('-avg_rating')

    # Latest anime
    anime = AnimeDB.objects.all().order_by('-id')

    # Most viewed anime
    counts = AnimeDB.objects.all().order_by('-views')


    username = request.session.get("Name")
    user = None
    if username:
        user = RegistrationDB.objects.filter(UserName=username).first()

    # Random Anime
    random_anime = AnimeDB.objects.all().order_by('?')[:3]
    random_animes = AnimeDB.objects.all().order_by('?')[:3]

    return render(request, 'HomePage.html', {
        'anime': anime,
        'counts': counts,
        'rating': rating,
        'random_anime': random_anime,
        'random_animes': random_animes,
        'user': user,
    })




def single_anime(request, anime_id):
    anime = get_object_or_404(AnimeDB, id=anime_id)
    anime.views += 1
    anime.save()

    comments = anime.comments.all().order_by('-created_at')
    rating_form = None
    user_rating = None
    comment_form = None
    user = None

    # Check if user is logged in
    username = request.session.get("Name")
    if username:
        user = RegistrationDB.objects.get(UserName=username)

        # Check if user already rated
        user_rating = RatingDB.objects.filter(anime=anime, user=user).first()

        if request.method == 'POST':
            if 'content' in request.POST:  # Comment form submitted
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.anime = anime
                    comment.user = user
                    comment.save()
                    return redirect('single_anime', anime_id=anime.id)

            elif 'value' in request.POST:  # Rating form submitted
                rating_form = RatingForm(request.POST, instance=user_rating)
                if rating_form.is_valid():
                    rating = rating_form.save(commit=False)
                    rating.anime = anime
                    rating.user = user
                    rating.save()
                    return redirect('single_anime', anime_id=anime.id)

        else:
            comment_form = CommentForm()
            rating_form = RatingForm(instance=user_rating)


    return render(request, 'SingleAnime.html', {
        'anime': anime,
        'comments': comments,
        'form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
        'average_rating': anime.average_rating(),
        'ratings_count': anime.ratings_count(),
        'user': user,  # None if not logged in
    })



def stream_anime(request,anime_id):
    anime = AnimeDB.objects.get(id=anime_id)
    return render(request,'StreamAnime.html',{'anime':anime})



def filter_anime(request, filter_type, filter_value):
    username = request.session.get("Name")
    if not username:
        return redirect("sign_in")

    user = get_object_or_404(RegistrationDB, UserName=username)
    random_anime = AnimeDB.objects.all().order_by('?')[:4]
    random_animes = AnimeDB.objects.all().order_by('?')[:4]

    anime = AnimeDB.objects.none()
    label = ""

    # Handle genre filtering
    if filter_type == "genre":
        genre = get_object_or_404(Genre, name=filter_value)
        anime = AnimeDB.objects.filter(genres__name=filter_value)
        label = genre.name

    # Handle version filtering (sub/dub)
    elif filter_type == "version":
        anime = AnimeDB.objects.filter(versions__icontains=filter_value)
        label = dict(AnimeDB.VERSION_CHOICES).get(filter_value, filter_value)

    # Handle type filtering (movie, ova, ona, tv series)
    elif filter_type == "type":
        filter_value = filter_value.replace("-", " ")
        anime = AnimeDB.objects.filter(type__iexact=filter_value)
        label = dict(AnimeDB.TYPE_CHOICES).get(filter_value, filter_value)

    return render(request, 'FilteredAnime.html', {
        'anime': anime,
        'filter_label': label,
        'user': user,
        'random_anime': random_anime,
        'random_animes': random_animes,
    })






def increment_views(request, anime_id):
    anime = get_object_or_404(AnimeDB, id=anime_id)
    anime.views += 1
    anime.save()
    return JsonResponse({"views": anime.views})



def sign_in(request):
    return render(request,'SignIn.html')

def sign_up(request):
    return render(request,'SignUp.html')

def save_user_reg(request):
    if request.method=="POST":
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        c_pwd = request.POST.get('c_password')
        obj = RegistrationDB(UserName=u_name,E_Mail =email,Password=pwd,C_Password=c_pwd)
        obj.save()
        return redirect(sign_in)

def user_login(request):
    if request.method=="POST":
        u_name = request.POST.get('username')
        pwd = request.POST.get('password')
        if RegistrationDB.objects.filter(UserName=u_name, Password=pwd).exists():
            request.session['Name'] = u_name
            request.session['Password'] = pwd
            return redirect(homepage)
        else:
            return redirect(sign_up)
    else:
        return redirect(sign_up)

def user_logout(request):
    request.session.pop('Name', None)
    request.session.pop('Password', None)
    return redirect(homepage)




def profile_page(request):
    username = request.session.get("Name")
    if not username:
        return redirect("sign_in")

    user = get_object_or_404(RegistrationDB, UserName=username)
    return render(request, "ProfilePage.html", {"user": user})


def watch_list(request):
    username = request.session.get("Name")
    if not username:
        return redirect("sign_in")

    user = get_object_or_404(RegistrationDB, UserName=username)

    # Get filter value from query parameter (e.g., ?category=watching)
    category = request.GET.get("category")

    watchlist = WatchListDB.objects.filter(user=user)
    if category:
        watchlist = watchlist.filter(category=category)

    return render(request, "WatchList.html", {
        "watchlist": watchlist,
        "selected_category": category,
        "user": user,
    })



def add_to_watchlist(request, anime_id):
    if request.method == "POST":
        category = request.POST.get("category")
        anime = get_object_or_404(AnimeDB, id=anime_id)

        # Get logged-in user from session (use 'Name')
        username = request.session.get("Name")
        if not username:
            return redirect("sign_in")

        # Fetch user by username
        user = get_object_or_404(RegistrationDB, UserName=username)

        # Save or update the watchlist entry
        obj, created = WatchListDB.objects.update_or_create(
            user=user,
            anime=anime,
            defaults={
                'category': category,
                'username': user.UserName,   # save username directly
                'anime_name': anime.Eng_Name  # save anime title directly
            }
        )

        return redirect("single_anime", anime_id=anime.id)

def remove_anime(request,Anime_ID):
    username = request.session.get("Name")
    if not username:
        return redirect("sign_in")
    user = get_object_or_404(RegistrationDB, UserName=username)

    # Delete the watchlist entry for this user + anime
    WatchListDB.objects.filter(user=user, anime_id=Anime_ID).delete()

    return redirect("watch_list")


from django.contrib import messages


def edit_profile_page(request):
    username = request.session.get("Name")
    if not username:
        return redirect("sign_in")

    user = get_object_or_404(RegistrationDB, UserName=username)

    if request.method == "POST":
        user.UserName = request.POST.get("username", user.UserName)
        user.E_Mail = request.POST.get("email", user.E_Mail)

        # update password only if provided
        current_pwd = request.POST.get("current_password")
        new_pwd = request.POST.get("new_password")
        confirm_pwd = request.POST.get("confirm_new_password")

        if new_pwd and confirm_pwd:
            if current_pwd == user.Password:  # verify current password
                if new_pwd == confirm_pwd:
                    user.Password = new_pwd
                    user.C_Password = confirm_pwd
                else:
                    messages.error(request, "New passwords do not match.")
                    return redirect("edit_profile_page")
            else:
                messages.error(request, "Current password is incorrect.")
                return redirect("edit_profile_page")

        # profile image
        if "avatar" in request.FILES:
            user.Profile_Image = request.FILES["avatar"]

        user.save()

        request.session["Name"] = user.UserName
        request.session["Password"] = user.Password

        messages.success(request, "Profile updated successfully!")
        return redirect("profile_page")

    return render(request, "ProfilePage.html", {"user": user})






