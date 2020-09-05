from flask import Flask, render_template
from newsapi import NewsApiClient


app = Flask(__name__)

@app.route('/')
def Index():
    newsapi = NewsApiClient(api_key="4f1b7a1d65744409b137d359d43c145b")
    topheadlines = newsapi.get_top_headlines(sources="buzzfeed")
    articles = topheadlines['articles']
    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img)
    return render_template("index.html", context=mylist)

@app.route('/bbc')
def bbc():
    newsapi = NewsApiClient(api_key="4f1b7a1d65744409b137d359d43c145b")
    topheadlines = newsapi.get_top_headlines(sources="bbc-news")
    articles = topheadlines['articles']
    desc = []
    news = []
    img = []

    for i in range(len(articles)):
        myarticles = articles[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])

    mylist = zip(news, desc, img)
    return render_template("bbc.html", context=mylist)

if __name__ == "__main__":
    app.run(debug=True)
