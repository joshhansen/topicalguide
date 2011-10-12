# The Topic Browser
# Copyright 2010-2011 Brigham Young University
#
# This file is part of the Topic Browser <http://nlp.cs.byu.edu/topic_browser>.
#
# The Topic Browser is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The Topic Browser is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with the Topic Browser.  If not, see <http://www.gnu.org/licenses/>.
#
# If you have inquiries regarding any further use of the Topic Browser, please
# contact the Copyright Licensing Office, Brigham Young University, 3760 HBLL,
# Provo, UT 84602, (801) 422-9339 or 422-3821, e-mail copyright@byu.edu.

from topic_modeling import anyjson
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods, require_GET
from topic_modeling.visualize.models import DatasetFavorite, Dataset, Analysis,\
    AnalysisFavorite
from django.core import serializers

class SerializerResponse(HttpResponse):
    def __init__(self, obj, fmt='json', *args, **kwargs):
        super(SerializerResponse, self).__init__(content=serializers.serialize(fmt, obj))

class JsonResponse(HttpResponse):
    def __init__(self, obj, *args, **kwargs):
        super(JsonResponse, self).__init__(anyjson.dumps(obj))

def _dataset_favorites(request):
    return DatasetFavorite.objects.filter(session_key=request.session.session_key)

@require_GET
def datasets(request):
    return SerializerResponse(_dataset_favorites(request))

@require_http_methods(['GET', 'PUT', 'DELETE'])
def dataset(request, dataset):
    dataset = Dataset.objects.get(name=dataset)
    
    def get():
        try:
            return DatasetFavorite.objects.get(dataset=dataset, session_key=request.session.session_key)
        except DatasetFavorite.DoesNotExist:
            return None
    
    def create():
        DatasetFavorite.objects.create(dataset=dataset, session_key=request.session.session_key)
    
    return _favorites_ajax_handler(request, get, create)

def _analysis_favorites(request, dataset=None):
    if dataset:
        return AnalysisFavorite.objects.filter(session_key=request.session.session_key, analysis__dataset__name=dataset)
    else:
        return AnalysisFavorite.objects.filter(session_key=request.session.session_key)

@require_GET
def analyses(request, **kwargs):
    if 'dataset' in kwargs:
        return SerializerResponse(_analysis_favorites(request, dataset=kwargs['dataset']))
    else:
        return SerializerResponse(_analysis_favorites(request))

@require_http_methods(['GET', 'PUT', 'DELETE'])
def analysis(request, dataset, analysis):
    analysis = Analysis.objects.get(name=analysis, dataset__name=dataset)
    
    def get():
        try:
            return AnalysisFavorite.objects.get(analysis=analysis, session_key=request.session.session_key)
        except AnalysisFavorite.DoesNotExist:
            return None
    
    def create():
        AnalysisFavorite.objects.create(analysis=analysis, session_key=request.session.session_key)
    
    return _favorites_ajax_handler(request, get, create)


'''
    {get} should return None if the favorite doesn't exist
'''
def _favorites_ajax_handler(request, get, create):
    fav = get()
    
    if request.method=='GET':
        fav_exists = fav is not None
        return JsonResponse(fav_exists)
    elif request.method=='PUT':
        if not fav:
            create()
        return JsonResponse(True)
    elif request.method=='DELETE':
        if fav:
            fav.delete()
        return JsonResponse(True)
    else:
        raise Exception("Unsupported HTTP method '" + request.method + "'")

#def index(request, dataset, analysis, id):
#    page_vars = dict()
#    page_vars['highlight'] = 'favorite_tab'
#    page_vars['tab'] = 'favorite'
#    page_vars['dataset'] = dataset
#    page_vars['analysis'] = analysis
#
#    page_vars['page_num'] = 1
#    page_vars['num_pages'] = 1
#    page_vars['favorites'] = request.session.get('favorite-set', set())
#
#    if id == '':
#        id = 0
#    else:
#        id = int(id)
#
#    page_vars['curr_favorite'] = None
#    for fav in page_vars['favorites']:
#        if fav.id == id:
#            page_vars['curr_favorite'] = fav
#
#    return render_to_response('favorite.html', page_vars)
#
#class Favorite:
#    def __init__(self, url, id, session, tab):
#        self.name = tab + ":" + url.split('/')[-1]
#        self.url = url
#        self.id = id
#        self.session_recall = {}
#        for key in session.keys():
#            if key.startswith(tab):
#                self.session_recall[key] = copy.deepcopy(session[key])
#        self.tab = tab
#
#    def __hash__(self):
#        return self.id
#
#    def __eq__(self, other):
#        return self.id == other.id
#
#    def __cmp__(self, other):
#        return self.id - other.id
#
##AJAX Calls
#def get_favorite_page(request, number):
#    ret_val = dict()
#    favorites = request.session.get('favorite-set', set())
#    ret_val['favorites'] = [{'id' : fav.id, 'name' : fav.name}
#                            for fav in favorites]
#    ret_val['num_pages'] = 1
#    ret_val['page'] = 1
#
#    return HttpResponse(anyjson.dumps(ret_val))
#
#def add_favorite(request, tab):
#    favorites = request.session.get('favorite-set', set())
#    id = request.session.get('last-favorite-id', 0)
#    url = request.GET['url']
#    favorite = Favorite(url, id, request.session, tab)
#    favorites.add(favorite)
#    request.session['last-favorite-id'] = favorite.id + 1
#    request.session['favorite-set'] = favorites
#    return HttpResponse('Favorite Added:' + favorite.url)
#
#def remove_all_favorites(request):
#    if 'favorite-set' in request.session:
#        request.session.remove('favorite-list')
#    return HttpResponse('Favorites cleared')
#
#def remove_favorite(request, url):
#    favorites = request.session.get('favorite-set', set())
#    if url in favorites:
#        favorites.remove(url)
#    request.session['favorite-set'] = favorites
#    return HttpResponse('Url Removed:' + url)
#
#def recall_favorite(request, id):
#    favorites = request.session.get('favorite-set', set())
#    id = int(id)
#    for favorite in favorites:
#        if favorite.id == id:
#            for key in favorite.session_recall.keys():
#                request.session[key] = copy.deepcopy(favorite.session_recall[key])
#            return HttpResponseRedirect(favorite.url)
#    return HttpResponse('Unknown Favorite')
