from flask import Flask, render_template, request, redirect
from search import search, getUniqueDetails

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/search')

@app.route('/search', methods=['GET', 'POST'])
def ui_search():
    ## get initial details
    res = getUniqueDetails()
    years = [ i["key"] for i in res["aggregations"]["year"]["buckets"] ]
    movies = [ i["key"] for i in res["aggregations"]["movie"]["buckets"] ]
    composers = [ i["key"] for i in res["aggregations"]["composer"]["buckets"] ]
    lyricists = [ i["key"] for i in res["aggregations"]["lyricist"]["buckets"] ]
    singers = [ i["key"] for i in res["aggregations"]["singer"]["buckets"] ]

    details = {"years"  : years, "movies": movies, "composers" : composers, "lyricists": lyricists, "singers" : singers}

    if request.method == 'POST':
        query = request.form['searchQuery']
        year = request.form['year']
        movie = request.form['movie']
        composer = request.form['composer']
        lyricist = request.form['lyricist']
        singer = request.form['singer']   
        yearmust =  True if "yearmust" in request.form else False
        moviemust =  True if "moviemust" in request.form else False
        composermust =  True if "composermust" in request.form else False
        lyricistmust =  True if "lyricistmust" in request.form else False
        singermust =  True if "singermust" in request.form else False
        

        res = search(query, year, yearmust, movie, moviemust, composer, composermust, lyricist, lyricistmust, singer, singermust)
        hits = res['hits']['hits']
        time = res['took']
        # aggs = res['aggregations']
        num_results =  res['hits']['total']['value']        
        return render_template('index.html', query=query, hits=hits, num_results=num_results,time=time, details = details)

    else:
        return render_template('index.html', init='True', details= details, num_results=0)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/search')

if __name__ == '__main__':
    app.run(debug=True)