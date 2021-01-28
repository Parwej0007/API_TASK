from django.shortcuts import render
import requests
from .models import Movie
from django.http import JsonResponse
from rest_framework import status
from django.db.models import Q

######### First Task #############
def movies_find(request):
    # checking request method
    if request.method=='POST':
        movie_title = request.POST['title_search']
        search_movi=Movie.objects.filter(title__contains=movie_title)
        # if search movie already exist then return movies details
        if search_movi:
            dict1 = {
                'Title': search_movi[0].title,
                'Year': search_movi[0].released_year,
                'Rating': search_movi[0].rating,
                'Genres': search_movi[0].genres,
                'movie_id': search_movi[0].movie_id
            }
            return JsonResponse(dict1, status=status.HTTP_200_OK)

        else:
            try:
            # call api if data in not available in your database and insert data in database
                response = requests.get(f"http://www.omdbapi.com/?apikey=CONTACTME&t={movie_title}")
                movie_data = response.json()
                dict1 = {
                    'Title': movie_data['Title'],
                    'Year': movie_data['Year'],
                    'Rating': movie_data['Rated'],
                    'Genres': movie_data['Genre'],
                    'movie_id': movie_data['imdbID']
                }
                m = Movie(title=dict1['Title'], released_year=dict1['Year'], rating=dict1['Rating'], genres=dict1['Genres'], movie_id=dict1['movie_id'])
                m.save()
                return JsonResponse(dict1, status=status.HTTP_200_OK)
            except:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    else:
        return render(request, 'search_movies_title.html')


######## second task ##########

def search_movies_data(request):
    if request.method=='POST':
        search = request.POST['search']
        # search data
        filt = Movie.objects.filter(
            Q(movie_id__contains=search)|Q(released_year__exact=search)|Q(genres__contains=search)|Q(title__contains=search)
        )
        list1 =[] # for storing value
        for data in filt:
            dict1= {}
            dict1['Title']=data.title
            dict1['Year']=data.released_year
            dict1['Rating'] = data.rating
            dict1['Genres'] = data.genres
            dict1['movies_id'] = data.movie_id
            list1.append(dict1)
        return JsonResponse({"Results":list1}, status=status.HTTP_200_OK)
    else:
        return render(request, 'search_data.html', )




