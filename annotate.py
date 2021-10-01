from bs4 import BeautifulSoup
from collections import defaultdict

class Transcript:
    def __init__(self, html) -> None:
        self.soup = BeautifulSoup(html, features = "lxml")

    def getCourses(self):
        courses = defaultdict(list)
        for row in self.soup.find_all("tr", class_ = "listRow"):
            courseName = row.find("td").get_text().split()
            courses[courseName[0]].append(courseName[1])
        return courses

# def getCourseNames(subjectCode, courseList):


tr = Transcript(open("transcript.html", "r"))
print(tr.getCourses())