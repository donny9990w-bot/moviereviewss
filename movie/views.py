import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import Movie
 
def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'name': 'Juan David Bedoya', 'searchTerm': searchTerm, 'movies': movies})
 
def about(request):
    return render(request, 'about.html')
 
def statistics(request):
    movies = Movie.objects.all()
 
    movie_counts_by_year = {}
    movie_counts_by_genre = {}
    for movie in movies:
        year = movie.year if movie.year else 'None'
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1
 
        genre = movie.genre.split(',')[0].strip() if movie.genre else 'None'
        movie_counts_by_genre[genre] = movie_counts_by_genre.get(genre, 0) + 1
 
    return render(request, 'statistics.html', {
        'graphic_year': _bar_chart(movie_counts_by_year, 'Year', 'Movies per year'),
        'graphic_genre': _bar_chart(movie_counts_by_genre, 'Genre', 'Movies per genre'),
    })
 
def _bar_chart(counts, xlabel, title):
    labels = [str(key) for key in counts.keys()]
    values = list(counts.values())
 
    plt.figure(figsize=(8, 4))
    plt.bar(range(len(values)), values, width=0.5, align='center')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Number of movies')
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
 
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
 