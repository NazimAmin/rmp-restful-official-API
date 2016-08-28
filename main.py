#!flask/bin/python
import json
import logging
from google.appengine.api import urlfetch
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)
RMP_BASE_URL = 'http://www.ratemyprofessors.com/api/professors/'
RMP_HEADERS = {
        'Content-Type' : 'application/json',
        'X-Auth-Token' : '20vkiiqon89ioc9ot##########',
    }
def get_school_id( name ):
    """
        Searches the given name
        :param name: school name to search
        :return: returns id or None
    """    
    url = 'http://search.mtvnservices.com//typeahead/suggest/?solrformat=true&q={0}&rows=500&defType=edismax&bq=schoolname_sort_s%3A%22baruch%22%5E1000&qf=schoolname_autosuggest&bf=pow%28total_number_of_ratings_i%2C1.9%29&sort=score%2Bdesc&siteName=rmp&rows=500&group=off&group.field=content_type_s&group.limit=500&fq=content_type_s%3ASCHOOL'.format(name.replace(' ', '%20'))
    return get_ids( url )
    
def get_prof_id( name , school_id=None):
    """
        Searches the given name
        :param name: name to search
        :return: returns id or None
    """
    if school_id == None:
        # by default search for stony brook professors
        school_id = '971'
    url = "http://search.mtvnservices.com/typeahead/suggest/?solrformat=true&q={0}%2BAND%2Bschoolid_s%3A{1}&defType=edismax&qf=teacherfullname_t%5E1000%2Bautosuggest&bf=pow%28total_number_of_ratings_i%2C2.1%29&sort=&siteName=rmp&rows=20&start=0&fl=pk_id%2Bteacherfirstname_t%2Bteacherlastname_t%2Btotal_number_of_ratings_i%2Baverageratingscore_rf%2Baverageclarityscore_rf%2Baveragehelpfulscore_rf%2Baverageeasyscore_rf%2Bchili_i%2Bschoolid_s".format(name.replace(' ', '%20'), school_id)
    return get_ids( url )

def get_ids(url):
    res = urlfetch.fetch(url, method='GET')
    pid = json.loads(res.content)
    pid = pid['response']['docs']
    return str(pid[0]['pk_id']) if len(pid) > 0 else None

def set_hot ( value ):
    """
        calculates the value to be used in 1/2/3 scale
        :return: 1/2/3
    """
    if value is not None:
        if value < 0:
            return 1
        elif 0 <= value <= 10:
            return 2
        else:
            return 3
        
def get_ratings ( url ):
    """
        Sends a GET request to the given URL
        :param url: url to request
        :return: returns JSON resonse 
            {avgEasiness: 2.5,
            avgRating: 4.6,
            chilliPepper: true,
            dept: "Computer Science",
            easinessText: "Fair",
            fName: " FIRST ",
            fullName: " FIRST LAST ",
            hotness: 34,
            id: 000000,
            lName: " LAST ",
            latesRatingDate: "2016-08-18T04:00:00Z",
            middleInitials: "",
            numOfRatings: 183,
            ratingText: "Awesome",
            school: "SOME SCHOOL",
            status: "Active",
            wouldTakeAgainPercent: 100
            }
    """
    res = urlfetch.fetch(url, method='GET', headers=RMP_HEADERS)
    res = json.loads(res.content)
    if 'hotness' in res: 
        res['hotness'] = set_hot(res['hotness']) 
    return res
    
@app.route('/<string:school>/<string:name>', methods = ['GET'])
@app.route('/<string:school>/<string:name>/<path:path>', methods = ['GET'])
def get_professor_rating( school=None, name=None, path=None ):
    """
        responds with the requested data
        :param name: name of the professor
        :param path: url path
        :return: ratings or error
    """
    if school is not None and name is not None:
        try:
            school_id = get_school_id(school)
            if school_id is not None:
                url = RMP_BASE_URL + get_prof_id( name, school_id )
                if path is not None:
                    if path == 'ratingsbyclass':
                        url = url + '/ratingsbyclass'
                    elif path == 'ratings':
                        url = url + '/ratings'
                    else:
                        abort(404)
                return jsonify( get_ratings( url ) )
            else: abort(404)
        except Exception as e:
            abort(404)    
    else:
        abort(404)
        
@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify( { 'err': 'Trust me it\'s not you. It\'s the developer!'} ), 500)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'err': 'No professor found that matches the given name' } ), 404)
if __name__ == '__main__':
    app.run(debug = True)