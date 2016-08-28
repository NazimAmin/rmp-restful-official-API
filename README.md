# rmp-restful-official-API
Rate my professor's official private API

Implimented to be used within the RateSBU extension
Sample GET requests: 

```javascript
GET /https://ratesbu-wrapper-api.appspot.com/stony brook university/ paul fodor
{
avgEasiness: 2.5,
avgRating: 4.6,
chilliPepper: true,
dept: "Computer Science",
easinessText: "Fair",
fName: "Paul",
fullName: "Paul Fodor",
hotness: 3,
id: 1614881,
lName: "Fodor",
latesRatingDate: "2016-08-18T04:00:00Z",
middleInitials: "",
numOfRatings: 183,
ratingText: "Awesome",
school: "Stony Brook University (SUNY)",
status: "Active",
tags: [
{
tagId: "1",
tagName: "Tough Grader"
},
...
,
{
tagId: "20",
tagName: "Lectures are long"
}
],
wouldTakeAgainPercent: 100
}
```
```javascript
GET /https://ratesbu-wrapper-api.appspot.com/stony%20brook%20university/%20paul%20fodor/ratings
{
count: 20,
ratingDetails: [
{
attendance: "non mandatory",
class: "CSE307",
comments: "Excellent professor! He respects student, and cares about them. The best professor I had. His lecture is organized, clear. Everything is in the slides you do not need a textbook. He is willing to help and is always there for you. He wants his students to learn and do well. Take all of his classes.",
easiness: 3,
helpfulness: 5,
interest: 0,
overallRating: 5,
ratedDate: "2016-08-18T19:01:15Z",
raterDepartments: [ ],
ratingText: "Awesome",
schoolId: "971",
standing: null,
teacherId: "1614881",
textbookUse: 0
} 
...
],
teacherInfo: {
...
tags: [ ... ],
wouldTakeAgainPercent: 100
}
}
```
```javascript
GET /https://ratesbu-wrapper-api.appspot.com/stony%20brook%20university/%20paul%20fodor/ratingsbyclass
[
{
attendancePerct: 0,
attendanceText: "Say Required",
classCode: "114",
classRating: 5,
count: 1,
ratingText: "Awesome",
textbookText: "Say Required",
textbookUsePerct: 100
},
...
{
attendancePerct: 100,
attendanceText: "Say Required",
classCode: "PHI105",
classRating: 3.5,
count: 1,
ratingText: "Good",
textbookText: "Say Required",
textbookUsePerct: 0
}
]
