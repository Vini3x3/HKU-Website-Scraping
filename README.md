# New Development

The version is created for two purpose: 

1. adding new functions in `HKUSites.py`: 

- Add `findContentByKeywords` function, which is `findCourseByKeywords` + `scrapeCourseContent`
- Add `findPageView` function, which is `findCourseByKeywords` + `scrapeCourseContentPreview`
- Add `findTable` function, which is work above `findInvoice`, `findReceipt`  and `findAccountActivtiy`

2. add notification module

- Auto notify when invoice is not paid
- Auto notify when lecture is near
- Auto notify when deadline is near