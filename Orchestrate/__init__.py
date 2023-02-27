# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json
import datetime
import azure.functions as func
import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    logging.info(f"Orchestrating")

    # year, month, day, hour, minute, second
    start_timestamp = datetime.datetime(2023, 1, 1, 0, 0, 0)
    end_timestamp   = datetime.datetime(2023, 1, 2, 0, 0, 0)

    start = int(start_timestamp.timestamp())
    end = int(end_timestamp.timestamp())

    logging.info(f"Initiating call_activity('GetTopPosts')")

    # durable functions call_activity with start and end parameters
    result = yield context.call_activity('GetTopPosts', {"start": start, "end": end})

    logging.info(f"call_activity('GetTopPosts') returned with {len(result)} items")

    # iterate over every item in the result
    for item in result:
        logging.info(f"item: {item}")

    return [result]

main = df.Orchestrator.create(orchestrator_function)
