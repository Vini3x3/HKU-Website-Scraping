# Extensions

After restructuring in Version 5, this version aims to complete the extension that covered by version 4.  

| Name                       | Site   | Input                                                        | Output                                     | Usage                                 |
| -------------------------- | ------ | ------------------------------------------------------------ | ------------------------------------------ | ------------------------------------- |
| getSiteMap                 | Moodle | None                                                         | list of tuples, `('name','link')`          | get the accessible course of the user |
| findCourseByKeywords       | Moodle | string                                                       | tuple, `('name', 'link')`                  | search course by keywords             |
| findAllCoursesByKeywords   | Moodle | string                                                       | list of tuples, `('name','link')`          | search courses by keywords            |
| scrapeCourseContents       | Moodle | string                                                       | list of dict, `{'link', 'name','type'}`    | get the content of the course         |
| scrapeCourseContentPreview | Moodle | string                                                       | filename of screenshot of the main content | get the preview of the course content |
| scrapeDeadlines            | Moodle | None                                                         | list of dict, `{'name','link', 'time'}`    | get the list of deadlines             |
| _getSiteMap_               | Portal | None                                                         | list of tuples, `('name','link')`          | list of links in the sidemenu         |
| findWeeklySchedule         | Portal | targetdate, starttime, endtime (string in dd/mm/yyyy format) | HTML string of the timetable               | get the weekly schedule of the user   |
| findTranscript             | Portal | None                                                         | dictionary with list of list (table)       | get information of that page          |
| findInvoice                | Portal | None                                                         | dictionary with list of list (table)       | get information of that page          |
| findReceipt                | Portal | None                                                         | dictionary with list of list (table)       | get information of that page          |
| findAccountActivity        | Portal | None                                                         | dictionary with list of list (table)       | get information of that page          |

