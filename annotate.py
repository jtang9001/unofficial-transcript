from bs4 import BeautifulSoup
from collections import defaultdict
import requests

class Transcript:
    def __init__(self, html) -> None:
        self.soup = BeautifulSoup(html, features = "lxml")
        self.getCourses()
        self.getCourseNames()

    def getCourses(self):
        self.coursesSorted = defaultdict(list)
        for row in self.soup.find_all("tr", class_ = "listRow"):
            courseName = row.find("td").get_text().split()
            self.coursesSorted[courseName[0]].append(courseName[1])
        return self.coursesSorted

    def getCourseNames(self):
        self.courses = {}        
        for subjectCode, courseNumbers in self.coursesSorted.items():
            url = f"http://www.calendar.ubc.ca/vancouver/courses.cfm?page=code&code={subjectCode}"
            r = requests.get(url)
            soup = BeautifulSoup(r.content, features="lxml")
            courseListings = [x.get_text() for x in soup.find_all("dt")]

            for courseNumber in courseNumbers:
                matchingCourses = [x.split(")")[1].lstrip() for x in courseListings if courseNumber in x]
                assert len(matchingCourses) == 1
                self.courses[f"{subjectCode}{courseNumber}"] = matchingCourses[0]
        return self.courses

    def fillCourseNames(self):
        for courseCode, courseTitle in self.courses.items():
            tag = self.soup.find("td", id=courseCode)
            print(tag)
            print(courseCode)
            print(courseTitle)
            tag.string = courseTitle
        with open("transcript_filled.html", "w", encoding="utf-8") as f:
            f.write(str(self.soup))
        

tr = Transcript(open("transcript.html", "r", encoding="utf-8"))
print(tr.getCourseNames())
tr.fillCourseNames()