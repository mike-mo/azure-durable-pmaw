
# Attempt at using PMAW in Azure Durable Functions

Basic Azure Durable Functions trigger, orchestrator, and single actiity function. The activity function uses PMAW to query Pushshift for Reddit submissions. Reddit functionality is provided as a repro for [https://github.com/mattpodolak/pmaw/issues/48](https://github.com/mattpodolak/pmaw/issues/48). See instructions below for how to reproduce.

References:

* https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode?tabs=windows&pivots=python-mode-configuration

  * https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash#v2

After instlaling the above and setting up a virtual environment, run the following to install the requirements:

`pip install -r .\\requirements.txt`

Enter your Reddit credentials in the `\\GetTopPosts\\__init__.py` file, lines 23-24.

----

When running the function, issuing a request to the function endpoint (typically at `http://localhost:7071/api/orchestrators/orchestrate`) will trigger the following error:

`System.Private.CoreLib: Exception while executing function: Functions.GetTopPosts. System.Private.CoreLib: Result: Failure
Exception: ValueError: signal only works in main thread of the main interpreter`

Full details below:

```

Found Python version 3.10.10 (py).

Azure Functions Core Tools
Core Tools Version:       4.0.5030 Commit hash: N/A  (64-bit)
Function Runtime Version: 4.15.2.20177


Functions:

        DurableFunctionsHttpStart: [POST,GET] http://localhost:7071/api/orchestrators/{functionName}

        GetTopPosts: activityTrigger

        Orchestrate: orchestrationTrigger

For detailed output, run func with --verbose flag.
[2023-02-27T05:30:19.669Z] Worker process started and initialized.
[2023-02-27T05:30:22.204Z] Host lock lease acquired by instance ID '00000000000000000000000095C50B72'.
[2023-02-27T05:47:46.152Z] Executing 'Functions.DurableFunctionsHttpStart' (Reason='This function was programmatically called via the host APIs.', Id=fed7a323-8650-4b68-a484-aaa5dc53df39)
[2023-02-27T05:47:46.990Z] Started orchestration with ID = '87a08d18a48f49c2bc7fe3602916d776'.
[2023-02-27T05:47:47.212Z] Executing 'Functions.Orchestrate' (Reason='(null)', Id=d0c6c64a-8905-434d-923c-f94537e9306c)
[2023-02-27T05:47:48.985Z] Orchestrating
[2023-02-27T05:47:48.987Z] Initiating call_activity('GetTopPosts')
[2023-02-27T05:47:49.006Z] Executed 'Functions.DurableFunctionsHttpStart' (Succeeded, Id=fed7a323-8650-4b68-a484-aaa5dc53df39, Duration=2867ms)
[2023-02-27T05:47:49.015Z] Executed 'Functions.Orchestrate' (Succeeded, Id=d0c6c64a-8905-434d-923c-f94537e9306c, Duration=1807ms)
[2023-02-27T05:47:49.177Z] Executing 'Functions.GetTopPosts' (Reason='(null)', Id=d8f80561-f773-4284-920e-41f471da6e6b)
[2023-02-27T05:47:49.195Z] GetTopPosts function started with input: {'start': 1672560000, 'end': 1672646400}. Logging into PRAW+PMAW...[2023-02-27T05:47:49.219Z]
 Reddit client created.

[2023-02-27T05:47:50.185Z] 7755 result(s) available in Pushshift
[2023-02-27T05:47:51.867Z] Executed 'Functions.GetTopPosts' (Failed, Id=d8f80561-f773-4284-920e-41f471da6e6b, Duration=2690ms)
[2023-02-27T05:47:51.870Z] System.Private.CoreLib: Exception while executing function: Functions.GetTopPosts. System.Private.CoreLib: Result: Failure
Exception: ValueError: signal only works in main thread of the main interpreter
Stack:   File "C:\\Program Files\\Microsoft\\Azure Functions Core Tools\\workers\\python\\3.10/WINDOWS/X64\\azure_functions_worker\\dispatcher.py", line 452, in _handle__invocation_request
    call_result = await self._loop.run_in_executor(
  File "C:\\Users\\devbox\\AppData\\Local\\Programs\\Python\\Python310\\lib\\concurrent\\futures\\thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
  File "C:\\Program Files\\Microsoft\\Azure Functions Core Tools\\workers\\python\\3.10/WINDOWS/X64\\azure_functions_worker\\dispatcher.py", line 718, in _run_sync_func
    return ExtensionManager.get_sync_invocation_wrapper(context,
  File "C:\\Program Files\\Microsoft\\Azure Functions Core Tools\\workers\\python\\3.10/WINDOWS/X64\\azure_functions_worker\\extension.py", line 215, in _raw_invocation_wrapper
    result = function(**args)
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\GetTopPosts\\__init__.py", line 38, in main
    all_submissions = pmaw_pushshift.search_submissions(subreddit=subreddit_name,
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\.venv\\lib\\site-packages\\pmaw\\PushshiftAPI.py", line 77, in search_submissions
    return self._search(kind="submission", **kwargs)
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\.venv\\lib\\site-packages\\pmaw\\PushshiftAPIBase.py", line 304, in _search
    self.req.check_sigs()
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\.venv\\lib\\site-packages\\pmaw\\Request.py", line 110, in check_sigs
    signal.signal(getattr(signal, "SIG" + sig), self._exit)
  File "C:\\Users\\devbox\\AppData\\Local\\Programs\\Python\\Python310\\lib\\signal.py", line 56, in signal
    handler = _signal.signal(_enum_to_int(signalnum), _enum_to_int(handler))
.
[2023-02-27T05:47:51.905Z] 87a08d18a48f49c2bc7fe3602916d776: Function 'GetTopPosts (Activity)' failed with an error. Reason: System.Exception:  ValueError: signal only works in main thread of the main interpreter
[2023-02-27T05:47:51.911Z]  ---> Microsoft.Azure.WebJobs.Script.Workers.Rpc.RpcException: Result: Failure
Exception: ValueError: signal only works in main thread of the main interpreter
Stack:   File "C:\\Program Files\\Microsoft\\Azure Functions Core Tools\\workers\\python\\3.10/WINDOWS/X64\\azure_functions_worker\\dispatcher.py", line 452, in _handle__invocation_request
    call_result = await self._loop.run_in_executor(
  File "C:\\Users\\devbox\\AppData\\Local\\Programs\\Python\\Python310\\lib\\concurrent\\futures\\thread.py", line 58, in run
    result = self.fn(*self.args, **self.kwargs)
  File "C:\\Program Files\\Microsoft\\Azure Functions Core Tools\\workers\\python\\3.10/WINDOWS/X64\\azure_functions_worker\\dispatcher.py", line 718, in _run_sync_func
    return ExtensionManager.get_sync_invocation_wrapper(context,
  File "C:\\Program Files\\Microsoft\\Azure Functions Core Tools\\workers\\python\\3.10/WINDOWS/X64\\azure_functions_worker\\extension.py", line 215, in _raw_invocation_wrapper
    result = function(**args)
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\GetTopPosts\\__init__.py", line 38, in main
    all_submissions = pmaw_pushshift.search_submissions(subreddit=subreddit_name,
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\.venv\\lib\\site-packages\\pmaw\\PushshiftAPI.py", line 77, in search_submissions
    return self._search(kind="submission", **kwargs)
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\.venv\\lib\\site-packages\\pmaw\\PushshiftAPIBase.py", line 304, in _search
    self.req.check_sigs()
  File "C:\\Users\\devbox\\Repos\\pmaw-signal\\.venv\\lib\\site-packages\\pmaw\\Request.py", line 110, in check_sigs
    signal.signal(getattr(signal, "SIG" + sig), self._exit)
  File "C:\\Users\\devbox\\AppData\\Local\\Programs\\Python\\Python310\\lib\\signal.py", line 56, in signal
    handler = _signal.signal(_enum_to_int(signalnum), _enum_to_int(handler))
```
