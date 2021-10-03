from bs4 import BeautifulSoup
from collections import defaultdict
import requests

class Transcript:
    def __init__(self, html) -> None:
        self.soup = BeautifulSoup(html, features = "lxml")

    def getCourses(self):
        courses = defaultdict(list)
        for row in self.soup.find_all("tr", class_ = "listRow"):
            courseName = row.find("td").get_text().split()
            courses[courseName[0]].append(courseName[1])
        return courses

def getCourseNames(subjectCode, courses):
    url = f"http://www.calendar.ubc.ca/vancouver/courses.cfm?page=code&code={subjectCode}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="lxml")
    courseListings = [x.get_text() for x in soup.find_all("dt")]
    
    for course in courses:
        matchingCourses = [x.split(")")[1].lstrip() for x in courseListings if course in x]
        assert len(matchingCourses) == 1
        print(matchingCourses)
    

tr = Transcript(open("transcript.html", "r"))
courseDict = tr.getCourses()

for subjectCode, courses in courseDict.items():
    getCourseNames(subjectCode, courses)