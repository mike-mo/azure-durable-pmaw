# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import praw
import pmaw
import datetime
import queue

def top_filter(submission):
  return submission['score'] >= 5000 and submission['removed_by'] == None and submission['removal_reason'] == None


def main(input: dict) -> list:
    logging.info(f"GetTopPosts function started with input: {input}. Logging into PRAW+PMAW...")

    # Initialize the Reddit API client
    reddit = praw.Reddit(client_id="REDDIT_CLIENT_ID",
                        client_secret="REDDIT_CLIENT_SECRET",
                        user_agent="python:pmaw-signal:v0.0.1-signal-bug")

    # Set up authentication credentials for PMAW
    pmaw_pushshift = pmaw.PushshiftAPI(praw=reddit)

    subreddit_name = "askreddit"

    logging.info("Reddit client created.")

    #print the current time
    execution_start = datetime.datetime.now()

    # Get submissions in subreddit
    all_submissions = pmaw_pushshift.search_submissions(subreddit=subreddit_name,
                                                        size=10,
                                                        filter_fn=top_filter,
                                                        since=input['start'],
                                                        until=input['end'])

    # use a PQ to sort the submissions by score
    top_submissions = queue.PriorityQueue()

    # Print the title and score of each submission
    for submission in all_submissions:
        logging.info(f"Passed potm_filter: ({submission['score']}) - {submission['title']}")

        # use creation time as a tiebreaker for submissions with the same score
        top_submissions.put((-submission['score'], submission['created_utc'], submission))

    # print out many seconds it took to get some posts since execution_start
    logging.info(f"Took {datetime.datetime.now() - execution_start} to get {top_submissions.qsize()} posts after filtering.")

    result = []

    # print some posts
    for i in range(5):
        post = top_submissions.get()

        # convert epoch time to datetime
        post_time = datetime.datetime.fromtimestamp(post[2]['created_utc'])
        logging.info(f"{i+1}. [{-post[0]}] {post[2]['title']} ({post_time})")

        # add post to result
        result.append(post[2])

    logging.info(f"Completed building result, returning to orchestrator.")

    return result
