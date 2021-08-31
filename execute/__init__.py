# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

import azure.functions as func
import azure.durable_functions as df
from azure.durable_functions.models.RetryOptions import RetryOptions


def orchestrator_function(context: df.DurableOrchestrationContext):
    retry_policy = RetryOptions(
        first_retry_interval_in_milliseconds=1500,
        max_number_of_attempts=3
    )

    tasks = [context.call_activity_with_retry('do', retry_options=retry_policy, input_=i) for i in range(100)]
    
    results = yield context.task_all(tasks)
    
    sorted_items = sorted(i for i in results if i is not None)
    missing_items = set(range(100)).difference(sorted_items)
    return {
        'sorted_len': len(sorted_items),
        'len_all': len(results),
        'missing_items': list(missing_items),
        'sorted_items': sorted_items,
        'items': results
    }

main = df.Orchestrator.create(orchestrator_function)