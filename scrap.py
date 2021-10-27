import requests
import io
from bs4 import BeautifulSoup

## This method will filter out any articles which are deemed inappropriate. If the header of the article contain any of the following words, they will be banned
def moniter(text):
    banned_words = ["partner","breast","boobs", "girlfriend","boyfriend", "bikini", "penis", "vagina", "sex", "prostitute", "hooker", "prostitution", "naked", "nude", "sexy", "underwear", "stripper", "porn", "WAGS", "wife"]
    verdict = "good"
    word = "Hi"
    for index in range(banned_words.__len__()):
        if(banned_words[index] in text):
            word = banned_words[index]
            verdict =  "bad"
    return verdict,word

## This method removes any wired non ascii code from strings
def remove_non_ascii(s):
    return "".join(c for c in s if ord(c)<128 )

# We will open the file we will be writing to
file = io.open("index.html", "w",encoding="utf-8")
# We will write basic html to the file
file.write('<html>\n')
file.write('<head>\n')
file.write('<title>SportsNews: A Personalized Version of Daily Mail Sports</title>\n')
file.write('<link rel=\"stylesheet\" href=\"style.css\">\n')
file.write(
    '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-15\" />\n')
file.write(
    '<center><h1 class = \"header\">SportsNews: A Personalized Version of Daily Mail Sports</h1></center>\n')
file.write('</head>\n')
file.write('<body>\n')


# We will set up the web scrapping
html = 'https://www.dailymail.co.uk/sport/football/index.html'
root = 'https://www.dailymail.co.uk'
source = requests.get(html).text
soup = BeautifulSoup(source, 'lxml')
articles = soup.find_all("a", {"itemprop": "url"})
count = articles.__len__()

front_images = BeautifulSoup(source, 'html.parser')
photo = front_images.find_all('div', class_="articletext")


for index in range(count):
    link = articles[index]['href']
    # We will check if the title of the story is suggestive in nature, if so, it will be blocked
    flagger,word = moniter(articles[index].text)
    if( flagger == "good"):
        # We will print out the title of the story
        file.write('<h2>\n')
        file.write(remove_non_ascii(articles[index].text))
        file.write('</h2>\n')
    

        checker = photo[index].find("img")
        if checker is not None and 'data-src' in checker.attrs:
            lead = (checker.attrs['data-src'])
            file.write("<center><img src = \"" + lead + "\"/img></center>\n")

        # We will piece up the full link of that story
        full_link = root + link

        # We will scrap the individual link of the story
        story = requests.get(full_link).text
        soup_2 = BeautifulSoup(story, 'lxml')

        file.write("<ul>")
        # This prints out the bullet points
        for bullet in soup_2.find_all("li", {"class": "class"}):
            file.write("<li>")
            file.write('<b>\n')
            file.write((remove_non_ascii(bullet.text)))
            file.write('</b>\n')
            file.write("</li>")
            file.write('<br>\n')
        file.write('</ul>\n')
        # This prints out the story
        for body in soup_2.find_all("p", {"class": "mol-para-with-font"}):
            file.write('<p>\n')
            file.write((remove_non_ascii(body.text)))
            file.write('<br>\n')
            file.write('</p>\n')
        file.write('<hr>\n')
        file.write('<br>\n')
    else:
        file.write("<p class = banned><b>This article is banned because the word \"" + word + "\" was detected\n</b></p>")
        file.write('<hr>\n')
        file.write('<br>\n')


file.write('\n')
file.write('</body>\n')
file.write('</html>\n')
file.close()





