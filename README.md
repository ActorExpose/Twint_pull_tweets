# Twint_pull_tweets
The code attempts to get around the problem of server disconnection while scraping tweets using Twint by automating retries. It does it in the following way:
1. It takes the input list of keywords or usernames that need to be scraped using Twint.
2. It takes the total duration of time (start_date and end_date) over which the tweets concerning the keywords need to be scraped, and it then
   divides this duration in time slots of period sizes. It uses the function make_periods to generate the list of time slots.
3. It then uses the function get_tweets for each keyword and each time slot and stores it into a csv file. This functions also stores and returns the keywords and
   timeslots that couldn"t be scraped due to server disconnection.
4. Finally, it asks the user to rerun the twint scraper for the uncollected keywords and timeslots. 
