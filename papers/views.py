from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .utils import get_papers
import pandas as pd

def home(request):
    """Render the home page with a search form."""
    return render(request, "papers/home.html")

def search_papers(request):
    """Handle search queries and display results."""
    query = request.GET.get("query", "")
    if not query:
        return render(request, "papers/home.html", {"error": "Please enter a search query."})

    df = get_papers(query)
    if df.empty:
        return render(request, "papers/home.html", {"error": "No relevant papers found."})

    return render(request, "papers/results.html", {"papers": df.to_dict(orient="records")})

def download_csv(request):
    """Allow users to download search results as a CSV file."""
    query = request.GET.get("query", "")
    if not query:
        return HttpResponse("No query provided.", status=400)

    df = get_papers(query)
    if df.empty:
        return HttpResponse("No relevant papers found.", status=404)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="papers_{query}.csv"'
    df.to_csv(response, index=False)
    return response
