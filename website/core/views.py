from core.essentials import SitesManager
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from core.models import Query

#List of proxies for Web Scrapping
# proxies = {
#  "http": "http://10.10.10.10:8000",
#  "https": "http://10.10.10.10:8000",
# }

# sitesmanager = SitesManager()

# Create your views here.
def index(request):
    context = {}
    template = get_template('index.html')
    r = HttpResponse(template.render(context, request))
    return r

def search(request):
    context = {}

    #Get the data
    keywords = request.GET.get('q')

    if keywords:
            results = Query.objects.all().filter(Keywords__contains=keywords)
            results.order_by('-Alexa_Rank')
            # context['Queries'] = results
            # context['Query'] = keywords
            # return HttpResponse(get_template('search.html').render(context, request))

            if len(results) == 0 or (int(len([i for i in results if (not keywords in i.title)])/len(results)*100) > 40):
                #Look for external help (lookup on google, yahoo, yandex, or/and bing)
                sitesmanager.scrape(keywords,type='Google')

                results = Query.objects.all().filter(Keywords__contains=keywords)
                results.order_by('-Alexa_Rank')
                context['Queries'] = results
                return HttpResponse(get_template('search.html').render(context, request))
            else:
                results = sorted(results, key=lambda x: x.Alexa_Rank)
                context['Queries'] = results
                context['Query'] = keywords
                return HttpResponse(get_template('search.html').render(context, request))
    else:
        response = redirect('/')
        return response
