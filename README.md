Search by website url using wikimedia api for search:
takes search queary and limit of pages. Search is occurence of search query in page.
the most reliable if company exists on wikipedia, but may lead to incorrect page if page just references comapny website in its text.

Search by company name using wikipediaapi library:
Try to find wikipedia page with exact company name. Exact company name is required, case sensitive, substrings like corp. must be removed in majority of the cases.

Search by company name using wikimedia api for search:
Request parameters same with search by website, results are ok since some companies have different names in wikipedia different from provided, but if company page does not exist leads to wrong page.

Most of the companies are under 'Construction_and_civil_engineering_companies_of {country name}' categories. Validating category after pulling pages greatly improves search.
Average search time 25-30 minutes. Think how to process websites asynchronously. Search by name gives ~60% of pages, but processing takes more time
With addition of search by language may increase up to 1-1.5 hours
Scrapping revenue from this urls takes several seconds.

Overall, 272 contractors were scraped with revenue data.

Pipeline is as follows:
1. Convert csv with company list to json and filter
2. Read company by line from json file
3. Process original company name by replacing spaces by _
4. Try to find it on wikipedia
5. If result is unsuccessful, clean name by removing prefixes (Co., etc)
6. If there is still no result, try to decapitalize name
7. Add entry to new json file
9. Run scrapy spider for contractors to fetch revenue
10. If revenue is not present in wiki, another script to use company website or provided website

I tried several approaches to gathering wikipedia company pages, stated above, but the most reliable
was to search by company name and search by category. It is not possible to do search by name in category, there is need
to gather all pages in category and pages in search by two requests, so it takes more time.

Initially only 157 companies found on wikipedia with revenue, then increased it to 211 by applying category filtering, 
and 272 was achieved by using English wiki along with Korean wiki. Using search in country's language wiki may increase 
this number to 500-700, I guess
Search by website url using wikimedia api for search:
takes search queary and limit of pages. Search is occurence of search query in page.
the most reliable if company exists on wikipedia, but may lead to incorrect page if page just references comapny website in its text.

Search by company name using wikipediaapi library:
Try to find wikipedia page with exact company name. Exact company name is required, case sensitive, substrings like corp. must be removed in majority of the cases.

Search by company name using wikimedia api for search:
Request parameters same with search by website, results are ok since some companies have different names in wikipedia different from provided, but if company page does not exist leads to wrong page.

Most of the companies are under 'Construction_and_civil_engineering_companies_of {country name}' categories. Validating category after pulling pages greatly improves search.
Average search time 25-30 minutes. Think how to process websites asynchronously. Search by name gives ~60% of pages, but processing takes more time
With addition of search by language may increase up to 1-1.5 hours
Scrapping revenue from this urls takes several seconds.

Overall, 272 contractors were scraped with revenue data.

Pipeline is as follows:
1. Convert csv with company list to json and filter
2. Read company by line from json file
3. Process original company name by replacing spaces by _
4. Try to find it on wikipedia
5. If result is unsuccessful, clean name by removing prefixes (Co., etc)
6. If there is still no result, try to decapitalize name
7. Add entry to new json file
9. Run scrapy spider for contractors to fetch revenue
10. If revenue is not present in wiki, another script to use company website or provided website

I tried several approaches to gathering wikipedia company pages, stated above, but the most reliable
was to search by company name and search by category. It is not possible to do search by name in category, there is need
to gather all pages in category and pages in search by two requests, so it takes more time.

Initially only 157 companies found on wikipedia with revenue, then increased it to 211 by applying category filtering, 
and 272 was achieved by using English wiki along with Korean wiki. Using search in country's language wiki may increase 
this number to 500-700, I guess
