import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from textblob import TextBlob

data = pd.read_csv(".\DataSets\IMDB\IMDB movies.csv")


def extractMovie(title):
    movieList = []
    limit = 20
    if len(title) < 3:
        for index in range(len(data["title"])):
            if limit:
                if data["title"][index].lower().startswith(title.lower()):
                    limit -= 1
                    movieList.append(
                        (index, data["title"][index], data["imdb_title_id"][index], data["genre"][index]))
            else:
                break

    else:
        for index in range(len(data["title"])):
            if limit:
                result = re.findall('\\b' + title.lower() + '\\b',
                                    data["title"][index].lower(), flags=re.IGNORECASE)
                if result:
                    limit -= 1
                    movieList.append(
                        (index, data["title"][index], data["imdb_title_id"][index], data["genre"][index]))
    movieList = scrapping(movieList)
    return movieList


def scrapping(movieList):
    movieDetails = []
    for movies in movieList:
        moviesDict = {}
        url = "https://www.imdb.com/title/" + movies[2]
        collection = requests.get(url)
        htmlContent = collection.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        title = soup.title
        title = title.string.split("(")
        movieTitle = title[0].strip()
        year = title[1].split(")")[0]
        image = soup.find(
            "div", class_="ipc-media ipc-media--poster ipc-image-media-ratio--poster ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img").img["src"].strip()
        try:
            rating = soup.find("div", {
                           "data-testid": "hero-rating-bar__aggregate-rating__score"}).find_all("span")[0].text.strip()
        except:
            pass
        moviesDict["imdbId"] = movies[2].strip()
        moviesDict["title"] = movieTitle
        moviesDict["year"] = year
        moviesDict["genre"] = movies[3].strip()
        moviesDict["imgSrc"] = image
        moviesDict["rating"] = rating
        movieDetails.append(moviesDict)
    return movieDetails


def googleScrap(title):
    movieDetails = {}
    title = title + " imdb"
    goog_search = "https://www.google.com/search?q=" + title
    r = requests.get(goog_search)

    soup = BeautifulSoup(r.text, "html.parser")
    movieTitle = soup.find_all('a')[16].text
    title = movieTitle.split("-")[0].strip()
    try:
        movieSrc = soup.find_all('a')[16]["href"]
        imdbId = movieSrc.split("www.imdb.com/title/")[1].split("/")[0]
    except:
        try:
            movieSrc = soup.find_all('a')[18]["href"]
            imdbId = movieSrc.split("www.imdb.com/title/")[1].split("/")[0]
        except:
            imdbId = None

    if imdbId:
        movieDetails["imdb_id"] = imdbId
        movieDetails["imdb_title"] = title
        return movieDetails

    return ""


def recommendation():
    movies = [("1", "Ludo", "tt7212754",  "Action, Comedy, Crime"), ("2", "Inception", "tt1375666",
                                                                     " Action, Adventure, Sci-Fi"), ("3", "Interstellar", "tt0816692", " Adventure, Drama, Sci-Fi")]
    return movies


def imdbMovieDetail(imdbId):
    movieData = []
    isSeries = False
    posterBlock = {}
    infoBlock = {}
    ratingBlock = {}
    reviewBlock = {}
    seriesBlock = {}
    url = "https://www.imdb.com/title/" + imdbId.strip()
    data = requests.get(url)
    htmlContent = data.content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    # poster
    try:
        posterSrc = soup.find(
            "div", class_="ipc-media ipc-media--poster ipc-image-media-ratio--poster ipc-media--baseAlt ipc-media--poster-l ipc-poster__poster-image ipc-media__img").img["src"].strip()
    except:
        posterSrc = "unknown"

    try:
        title = soup.title
        year = soup.find("span", {"id": "titleYear"}).text.strip()
        movieTitle = title.string.split("(")[0].strip() + year
    except:
        movieTitle = title.string.split("(")[0].strip()

    try:
        summary = soup.find("div", {"data-testid": "storyline-plot-summary"}
                            ).div.div.text.strip()
    except:
        summary = "Currently storyline of this movie is not available."

    # Info block

    try:
        director = soup.find("div", {"data-testid": "title-pc-wide-screen"}).find_all(
            "ul")[0].find_all("li")[0].text.split("Director")[1].strip()

    except:
        director = "Unknown"

    genre = ""
    try:
        test = soup.find(
            "li", {"data-testid": "storyline-genres"}).find_all("li")
        genre = test[0].text.strip()
        for item in test[1:]:
            genre += ", " + item.text.strip()
    except:
        genre = "Unknown"

    try:
        tagline = soup.find(
            "li", {"data-testid": "storyline-taglines"}).find_all("li")[0].text.strip()
    except:
        tagline = "Unknown"

    try:
        test = soup.find(
            "li", {"data-testid": "title-details-languages"}).find_all("li")
        languages = test[0].text.strip()
        for item in test[1:]:
            languages += ", " + item.text.strip()
    except:
        languages = "unknown"

    try:
        country = soup.find(
            "li", {"data-testid": "title-details-origin"}).find_all("li")[0].text.strip()
    except:
        country = "unknown"

    try:
        test = soup.find(
            "li", {"data-testid": "title-details-officialsites"}).find_all("li")
        sites = test[0].text.strip()
        for item in test[1:]:
            sites += ", " + item.text.strip()
    except:
        sites = "unknown"

    result = ["Unknown" for _ in range(3)]
    try:
        test = soup.find("div", class_="TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"
                         ).find_all("ul")[0].find_all("li")
        i = 0
        for val in test:
            if i < 2:
                result[i] = (val.find_all("span")[0].text)
            else:
                result[i] = (val.text)
            i += 1
            if i == 3:
                break
    except:
        pass
    year, certi, duration = result[0], result[1], result[2]
    if year != "Unknown":
        movieTitle += " " + year

    try:
        trivia = soup.find(
            "div", class_="ipc-html-content ipc-html-content--base DidYouKnowCard__StyledHTMLContent-sc-1aia7w-0 jANtvU").div.text.strip()

    except:
        trivia = "Not Available"

    # rating block

    try:
        rating = soup.find("div", {
                           "data-testid": "hero-rating-bar__aggregate-rating__score"}).find_all("span")[0].text.strip()
    except:
        rating = "Average"

    try:
        usersVote = soup.find("div", {
                              "data-testid": "hero-rating-bar__aggregate-rating__score"}).parent.find_all("div")[2].text.strip()
    except:
        usersVote = "Undefined"

    try:
        released = soup.find(
            "li", {"data-testid": "title-details-releasedate"}).find_all("li")[0].text.strip()
    except:
        released = "Unknown"

    # cast block

    # ext = "._V1_UY317_CR3,0,214,317_AL__QL50.jpg"
    try:
        test4 = soup.find("div", {
                      "class": "ipc-sub-grid ipc-sub-grid--page-span-2 ipc-sub-grid--wraps-at-above-l ipc-shoveler__grid"}).find_all("div", {
                          "data-testid": "title-cast-item"})
    except:
        test4 = []
    cast = []
    for val in test4:
        dic = {}
        if val.text.strip().find("Rest of cast listed alphabetically:") == -1:
            try:
                finalImg = val.find("img")['src']
                # finalImg = img.split("._V1")[0] + ext
            except:
                finalImg = "Unknown"

            try:
                name = val.find(
                    "a", {"data-testid": "title-cast-item__actor"}).text.strip()
            except:
                name = "Unknown"
            try:
                # role = val.find("div", {"class": "title-cast-item__characters-list"}).find_all("ul", {"data-testid": "cast-item-characters-list"})[0].find_all("li", {'class': "ipc-inline-list__item"}).find_all("a")[
                #     0].find_all("span")[0].text.strip()
                role = val.find(
                    "div", {"class": "title-cast-item__characters-list"}).find_all("ul", {"data-testid": "cast-item-characters-list"})[0].text.split("as ")[0].strip()

            except:
                role = "Unknown"

            if name == "Unknown":
                pass
            else:
                dic["name"] = name
                dic["role"] = role
                dic["imgSrc"] = finalImg
                cast.append(dic)

    # making review contents.
    try:
        revHeader = soup.find(
            "span", {"data-testid": "review-summary"}).text.strip()
    except:
        revHeader = "No comments available"

    try:
        test = soup.find(
            "div", {"data-testid": "reviews-author"}).ul.find_all("li")
        revOwner = test[0].text + " " + test[1].text
    except:
        revOwner = director

    try:
        revDesc = soup.find(
            "div", {"data-testid": "review-overflow"}).text.strip()
    except:
        revDesc = summary

    # sentimental analysis
    blob = TextBlob(revHeader + " " + revDesc)

    sentiments = blob.sentiment.polarity
    print(sentiments)

    if sentiments >= 0.8:
        sentiments = "Awesome"
        revImgSrc = "1"
    elif sentiments >= 0.5 and sentiments < 0.8:
        sentiments = "Very Good"
        revImgSrc = "2"
    elif sentiments >= 0.01 and sentiments < 0.5:
        sentiments = "Good"
        revImgSrc = "3"
    elif sentiments < 0.01 and sentiments > -0.5:
        sentiments = "Bad"
        revImgSrc = "4"
    else:
        sentiments = "Awful"
        revImgSrc = "5"

    # season Block
    try:
        episodes = soup.find("span", class_="bp_sub_heading").text.strip()
        seasons = soup.find(
            "div", class_="seasons-and-year-nav").find_all("div")[2].find_all("a")[0].text.strip()
        isSeries = True
    except:
        episodes = ""
        seasons = ""

    # making dict
    posterBlock["poster"] = posterSrc
    posterBlock["title"] = movieTitle
    posterBlock["summary"] = summary

    seriesBlock["episodes"] = episodes
    seriesBlock["seasons"] = seasons
    seriesBlock["isSeries"] = isSeries

    infoBlock["director"] = director
    infoBlock["category"] = genre
    infoBlock["tagline"] = tagline
    infoBlock["languages"] = languages
    infoBlock["country"] = country
    infoBlock["sites"] = sites
    infoBlock["certi"] = certi
    infoBlock["trivia"] = trivia

    ratingBlock["rating"] = rating
    ratingBlock["userVote"] = usersVote
    ratingBlock["duration"] = duration
    ratingBlock["released"] = released

    reviewBlock["header"] = revHeader
    reviewBlock["description"] = revDesc
    reviewBlock["owner"] = revOwner
    reviewBlock["sentiments"] = sentiments
    reviewBlock["logo"] = revImgSrc

    movieData.append(posterBlock)
    movieData.append(infoBlock)
    movieData.append(ratingBlock)
    movieData.append(cast)
    movieData.append(reviewBlock)
    movieData.append(seriesBlock)

    return movieData
