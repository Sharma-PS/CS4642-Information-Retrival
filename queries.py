import json

def standard_analyzer(query):
    q = {
        "analyzer": "standard",
        "text": query
    }
    return q


def basic_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "highlight": {
            "fields": {
                "பாடல்வரிகள்": {}
            },
            "pre_tags" : "<i>",
            "post_tags" : "</i>"
        },
        "size": 150
    }
    return q

def advanced_search(query, year, yearmust, movie, moviemust, composer, composermust, lyricist, lyricistmust, singer, singermust):
    should = []
    must = []
    
    should.append({"query_string": { "query": query }})

    if year != "" and yearmust:
        must.append({ "match": { "வருடம்": year } })
    elif year != "":
        should.append({ "match": { "வருடம்": year } })

    if movie != "" and moviemust:
        must.append({"match": { "படம்": movie }})
    elif movie != "":
        should.append({"match": { "படம்": movie }})

    if composer != "" and composermust:
        must.append({"match": { "இசை": composer }})
    elif composer != "" :
        should.append({"match": { "இசை": composer }})

    if lyricist != "" and lyricistmust:
        must.append({"match": { "பாடலாசிரியர்": lyricist }})
    elif lyricist != "":
        should.append({"match": { "பாடலாசிரியர்": lyricist }})

    if singer != "" and singermust:
        must.append({"match": { "பாடகர்": singer }})
    elif singer != "":
        should.append({"match": { "பாடகர்": singer }})

    q = {
        "query": {            
            "bool": {
                "should": should,
                "must" : must       
            },
        },
        "size": 100
    }     
    print(query, year, yearmust, movie, moviemust, composer, composermust, lyricist, lyricistmust, singer, singermust)
    return q


def search_with_field(query, field):
    q = {
        "query": {
            "match": {
                [field]: query
            }
        }
    }
    return q


def multi_match(query, fields=['title', 'song_lyrics'], operator='or'):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    return q

def get_unique_values():
    q = {
        "size" : 0,
        "aggs" : {
            "year":{
                "terms":{
                    "field" : "வருடம்",
                    "order" : {
                        "_key" : "asc"
                    },
                    "size" : 100
                }
            },
            "movie":{
                "terms":{
                    "field" : "படம்.keyword",                
                    "size" : 100,
                    "order" : {
                        "_key" : "asc"
                    },
                }
            },    
            "composer":{
                "terms":{
                    "field" : "இசை.keyword",
                    "order" : {
                        "_key" : "asc"
                    },
                    "size" : 100
                }
            },
            "lyricist":{
                "terms":{
                    "field" : "பாடலாசிரியர்.keyword",                
                    "size" : 100,
                    "order" : {
                        "_key" : "asc"
                    },
                }
            },
            "singer":{
                "terms":{
                    "field" : "பாடகர்.keyword",                
                    "size" : 100,
                    "order" : {
                        "_key" : "asc"
                    },
                }
            }      
        }
    }
    return q


def agg_multi_match_q(query, fields=['title', 'song_lyrics'], operator='or'):
    q = {
        "size": 500,
        "explain": True,
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "operator": operator,
                "type": "best_fields"
            }
        },
        "aggs": {
            "Genre Filter": {
                "terms": {
                    "field": "genre.keyword",
                    "size": 10
                }
            },
            "Music Filter": {
                "terms": {
                    "field": "music.keyword",
                    "size": 10
                }
            },
            "Artist Filter": {
                "terms": {
                    "field": "artist.keyword",
                    "size": 10
                }
            },
            "Lyrics Filter": {
                "terms": {
                    "field": "lyrics.keyword",
                    "size": 10
                }
            }
        }
    }

    q = json.dumps(q)
    return q