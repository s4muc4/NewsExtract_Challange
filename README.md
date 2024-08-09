

# 🟢 The Challenge #

#### I'm using https://www.latimes.com/ to extract news. ####


## Parameters


- search phrase

- news category/section/topic

- number of months for which you need to receive news (if applicable)

  - Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on

If run locally, use `work-items.json`.

If run via robocorp workitens, follow some suggestions

```
{
  "data": {
    "phrase": "Artificial Inteligence",
    "sort_by": "Newest",
    "history": "0"
  }
}
```
```
{
  "data": {
    "phrase": "Car",
    "sort_by": "Newest",
    "history": "1"
  }
}
```
```
{
  "data": {
    "phrase": "Olympics",
    "sort_by": "Newest",
    "history": "2"
  }
}
```

## The Process
The main steps:

1 - Open the site by following the link

2 - Enter a phrase in the search field

3 - On the result page

- If possible select a news category or section from the

- Choose the latest (i.e., newest) news

4 - Get the values: title, date, and description.

5 - Store in an Excel file:

- title

- date

- description (if available)

- picture filename

- count of search phrases in the title and description

- True or False, depending on whether the title or description contains any amount of money

  - Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD

6 - Download the news picture and specify the file name in the Excel file

7 - Follow steps 4-6 for all news that falls within the required time period

### 🎁 - BONUS - Using textblob to analyse sentiment of each description (polarity and subjectivity)
Polarity - Range: [-1.0, 1.0], where -1.0 is very negative and 1.0 is very positive
Subjectivity - Range: [0.0, 1.0], where 0.0 is very objective and 1.0 is very subjective
All of these saved in excel file

 
## Requirements

All steps working ✅

Using PEP8 compliant ✅

Using OOP ✅

Using explicit waits ✅

Using logging ✅

Using string formatting ✅

Do not using APIs or Web Requests ✅

Using pure python, and not robot framework ✅

Using rpaframework ✅

Using Selenium ✅

Repo integrated with Robocloud ✅