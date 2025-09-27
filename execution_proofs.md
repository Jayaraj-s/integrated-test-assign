# Proofs

## Logs

```bash
anish@DESKTOP-9C4N1VG:~/integrated-test-assign$ uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/home/anish/integrated-test-assign']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [51851] using StatReload
INFO:     Started server process [51853]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50324 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:49658 - "POST /auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:35900 - "POST /auth/login HTTP/1.1" 200 OK
INFO:     127.0.0.1:58814 - "POST /items HTTP/1.1" 200 OK
INFO:     127.0.0.1:53120 - "GET /items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58430 - "PUT /items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58434 - "GET /items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54296 - "GET /items HTTP/1.1" 200 OK
INFO:     127.0.0.1:33024 - "DELETE /items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56634 - "GET /items HTTP/1.1" 200 OK
```


## Terminal Input & Output

```bash
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X POST "http://127.0.0.1:8000/auth/login"   -H "Content-Type: application/json"   -d '{"username":"admin","password":"adminPass"}'
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YBY","token_type":"bearer","expires_at":1758970200}
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X POST "http://127.0.0.1:8000/items" \                              curl -X POST "http://127.0.0.1:8000/items" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YBY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Item1","value":"Value1"}'
{"name":"Item1","value":"Value1","id":"8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7"}
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X GET "http://127.0.0.1:8000/items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YBY"
{"name":"Item1","value":"Value1","id":"8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7"}
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X PUT "http://127.0.0.1:8000/items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6ecurl -X PUT "http://127.0.0.1:8000/items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YBY" \
  -H "Content-Type: application/json" \
  -d '{"name":"UpdatedItem","value":"UpdatedValue"}'
{"name":"UpdatedItem","value":"UpdatedValue","id":"8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7"}
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X GET "http://127.0.0.1:8000/items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7"   -H "Authorization: Bearer eyJhbGciOiJIU
zI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YB
Y"
{"name":"UpdatedItem","value":"UpdatedValue","id":"8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7"}
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X GET "http://127.0.0.1:8000/items" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YBY"
[{"name":"UpdatedItem","value":"UpdatedValue","id":"8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7"}]
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X DELETE "http://127.0.0.1:8000/items/8fa62768-07eb-4eb3curl -X DELETE "http://127.0.0.1:8000/items/8fa62768-07eb-4eb3-b1f8-bcb75c85f6e7" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YBY"
{"deleted":true}
(.venv) anish@DESKTOP-9C4N1VG:~$ curl -X GET "http://127.0.0.1:8000/items"   -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTc1ODk2NjYwMCwiZXhwIjoxNzU4OTcwMjAwfQ.78X47Zgh8SKreRMzvyp5uk8O67hzvAPfsUvLPhr3YBY"
(.venv) anish@DESKTOP-9C4N1VG:~$ 
```

## Tests
1. Integration Tests(Security Tests, Performance Tests, EdgeCases)
1. Performance Tests

### Coverage

```bash
(.venv) anish@DESKTOP-9C4N1VG:~/integrated-test-assign$ pytest --cov=services --cov=main --cov-report=term-missing
================================================================== test session starts ==================================================================
platform linux -- Python 3.12.3, pytest-8.4.2, pluggy-1.6.0
rootdir: /home/anish/integrated-test-assign
plugins: xdist-3.8.0, httpx-0.35.0, cov-7.0.0, anyio-4.11.0, asyncio-1.2.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 62 items                                                                                                                                      

tests/test_auth.py ........................                                                                          [ 38%]
tests/test_performance.py ...                                                                                        [ 43%]
tests/test_storage_api.py ...................................                                                        [100%]

=================================================================== warnings summary ====================================================================
tests/test_storage_api.py:588
  /home/anish/integrated-test-assign/tests/test_storage_api.py:588: PytestUnknownMarkWarning: Unknown pytest.mark.slow - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.slow  # Mark as slow test

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
==================================================================== tests coverage =====================================================================
____________________________________________________ coverage: platform linux, python 3.12.3-final-0 ____________________________________________________

Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
main.py                          11      1    91%   18
services/__init__.py              0      0   100%
services/auth_service.py         55      0   100%
services/storage_service.py      41      0   100%
-----------------------------------------------------------
TOTAL                           107      1    99%
```

## Gitlab Pipeline run 

1. Repo: https://gitlab.com/Jayaraj-s/integrated-test-assign
1. Jobs: https://gitlab.com/Jayaraj-s/integrated-test-assign/-/jobs/11521669399

### Job Log
```bash
Running with gitlab-runner 18.4.0~pre.115.gb2218bab (b2218bab)
  on blue-6.saas-linux-small-amd64.runners-manager.gitlab.com/default nN8vMRS9Z, system ID: s_a899fcd611a3
Preparing the "docker+machine" executor
00:21
Using Docker executor with image python:3.12 ...
Using effective pull policy of [always] for container python:3.12
Pulling docker image python:3.12 ...
Using docker image sha256:48374675bfb70b70165ff4a6783d23c80b8e8c71d14dfda6edb4aaedf49bfe78 for python:3.12 with digest python@sha256:1cb6108b64a4caf2a862499bf90dc65703a08101e8bfb346a18c9d12c0ed5b7e ...
Preparing environment
00:06
Using effective pull policy of [always] for container sha256:292f5adc909b743340a8e8b3da383da6d547c481bceac8e1fd1fd634242c5fc5
Running on runner-nn8vmrs9z-project-74811778-concurrent-0 via runner-nn8vmrs9z-s-l-s-amd64-1758966058-e58ebf74...
Getting source from Git repository
00:01
Gitaly correlation ID: 0777908132274549b18bd425294a63bc
Fetching changes with git depth set to 20...
Initialized empty Git repository in /builds/Jayaraj-s/integrated-test-assign/.git/
Created fresh repository.
Checking out 458b4c91 as detached HEAD (ref is main)...
Skipping Git submodules setup
$ git remote set-url origin "${CI_REPOSITORY_URL}" || echo 'Not a git repository; skipping'
Restoring cache
00:01
Checking cache for default-protected...
Downloading cache from https://storage.googleapis.com/gitlab-com-runners-cache/project/74811778/default-protected  ETag="aeb5ab5cce03089a28174f26f0787b0b"
Successfully extracted cache
Executing "step_script" stage of the job script
00:15
Using effective pull policy of [always] for container python:3.12
Using docker image sha256:48374675bfb70b70165ff4a6783d23c80b8e8c71d14dfda6edb4aaedf49bfe78 for python:3.12 with digest python@sha256:1cb6108b64a4caf2a862499bf90dc65703a08101e8bfb346a18c9d12c0ed5b7e ...
$ python -V
Python 3.12.11
$ pip install --upgrade pip
Requirement already satisfied: pip in /usr/local/lib/python3.12/site-packages (25.0.1)
Collecting pip
  Using cached pip-25.2-py3-none-any.whl.metadata (4.7 kB)
Using cached pip-25.2-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 25.0.1
    Uninstalling pip-25.0.1:
      Successfully uninstalled pip-25.0.1
Successfully installed pip-25.2
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
$ pip install -r requirements.txt
Collecting fastapi (from -r requirements.txt (line 1))
  Using cached fastapi-0.117.1-py3-none-any.whl.metadata (28 kB)
Collecting uvicorn (from -r requirements.txt (line 2))
  Using cached uvicorn-0.37.0-py3-none-any.whl.metadata (6.6 kB)
Collecting PyJWT (from -r requirements.txt (line 3))
  Using cached PyJWT-2.10.1-py3-none-any.whl.metadata (4.0 kB)
Collecting requests (from -r requirements.txt (line 4))
  Using cached requests-2.32.5-py3-none-any.whl.metadata (4.9 kB)
Collecting httpx (from -r requirements.txt (line 5))
  Using cached httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting pytest (from -r requirements.txt (line 6))
  Using cached pytest-8.4.2-py3-none-any.whl.metadata (7.7 kB)
Collecting pytest-httpx (from -r requirements.txt (line 7))
  Using cached pytest_httpx-0.35.0-py3-none-any.whl.metadata (35 kB)
Collecting pytest-asyncio (from -r requirements.txt (line 8))
  Using cached pytest_asyncio-1.2.0-py3-none-any.whl.metadata (4.1 kB)
Collecting pytest-cov (from -r requirements.txt (line 9))
  Using cached pytest_cov-7.0.0-py3-none-any.whl.metadata (31 kB)
Collecting pytest-xdist (from -r requirements.txt (line 10))
  Using cached pytest_xdist-3.8.0-py3-none-any.whl.metadata (3.0 kB)
Collecting pydantic (from -r requirements.txt (line 11))
  Using cached pydantic-2.11.9-py3-none-any.whl.metadata (68 kB)
Collecting gunicorn (from -r requirements.txt (line 12))
  Using cached gunicorn-23.0.0-py3-none-any.whl.metadata (4.4 kB)
Collecting starlette<0.49.0,>=0.40.0 (from fastapi->-r requirements.txt (line 1))
  Using cached starlette-0.48.0-py3-none-any.whl.metadata (6.3 kB)
Collecting typing-extensions>=4.8.0 (from fastapi->-r requirements.txt (line 1))
  Using cached typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Collecting annotated-types>=0.6.0 (from pydantic->-r requirements.txt (line 11))
  Using cached annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.33.2 (from pydantic->-r requirements.txt (line 11))
  Using cached pydantic_core-2.33.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (6.8 kB)
Collecting typing-inspection>=0.4.0 (from pydantic->-r requirements.txt (line 11))
  Using cached typing_inspection-0.4.1-py3-none-any.whl.metadata (2.6 kB)
Collecting anyio<5,>=3.6.2 (from starlette<0.49.0,>=0.40.0->fastapi->-r requirements.txt (line 1))
  Using cached anyio-4.11.0-py3-none-any.whl.metadata (4.1 kB)
Collecting idna>=2.8 (from anyio<5,>=3.6.2->starlette<0.49.0,>=0.40.0->fastapi->-r requirements.txt (line 1))
  Using cached idna-3.10-py3-none-any.whl.metadata (10 kB)
Collecting sniffio>=1.1 (from anyio<5,>=3.6.2->starlette<0.49.0,>=0.40.0->fastapi->-r requirements.txt (line 1))
  Using cached sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting click>=7.0 (from uvicorn->-r requirements.txt (line 2))
  Using cached click-8.3.0-py3-none-any.whl.metadata (2.6 kB)
Collecting h11>=0.8 (from uvicorn->-r requirements.txt (line 2))
  Using cached h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting charset_normalizer<4,>=2 (from requests->-r requirements.txt (line 4))
  Using cached charset_normalizer-3.4.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (36 kB)
Collecting urllib3<3,>=1.21.1 (from requests->-r requirements.txt (line 4))
  Using cached urllib3-2.5.0-py3-none-any.whl.metadata (6.5 kB)
Collecting certifi>=2017.4.17 (from requests->-r requirements.txt (line 4))
  Using cached certifi-2025.8.3-py3-none-any.whl.metadata (2.4 kB)
Collecting httpcore==1.* (from httpx->-r requirements.txt (line 5))
  Using cached httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting iniconfig>=1 (from pytest->-r requirements.txt (line 6))
  Using cached iniconfig-2.1.0-py3-none-any.whl.metadata (2.7 kB)
Collecting packaging>=20 (from pytest->-r requirements.txt (line 6))
  Using cached packaging-25.0-py3-none-any.whl.metadata (3.3 kB)
Collecting pluggy<2,>=1.5 (from pytest->-r requirements.txt (line 6))
  Using cached pluggy-1.6.0-py3-none-any.whl.metadata (4.8 kB)
Collecting pygments>=2.7.2 (from pytest->-r requirements.txt (line 6))
  Using cached pygments-2.19.2-py3-none-any.whl.metadata (2.5 kB)
Collecting coverage>=7.10.6 (from coverage[toml]>=7.10.6->pytest-cov->-r requirements.txt (line 9))
  Using cached coverage-7.10.7-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (8.9 kB)
Collecting execnet>=2.1 (from pytest-xdist->-r requirements.txt (line 10))
  Using cached execnet-2.1.1-py3-none-any.whl.metadata (2.9 kB)
Using cached fastapi-0.117.1-py3-none-any.whl (95 kB)
Using cached pydantic-2.11.9-py3-none-any.whl (444 kB)
Using cached pydantic_core-2.33.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.0 MB)
Using cached starlette-0.48.0-py3-none-any.whl (73 kB)
Using cached anyio-4.11.0-py3-none-any.whl (109 kB)
Using cached uvicorn-0.37.0-py3-none-any.whl (67 kB)
Using cached PyJWT-2.10.1-py3-none-any.whl (22 kB)
Using cached requests-2.32.5-py3-none-any.whl (64 kB)
Using cached charset_normalizer-3.4.3-cp312-cp312-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (151 kB)
Using cached idna-3.10-py3-none-any.whl (70 kB)
Using cached urllib3-2.5.0-py3-none-any.whl (129 kB)
Using cached httpx-0.28.1-py3-none-any.whl (73 kB)
Using cached httpcore-1.0.9-py3-none-any.whl (78 kB)
Using cached pytest-8.4.2-py3-none-any.whl (365 kB)
Using cached pluggy-1.6.0-py3-none-any.whl (20 kB)
Using cached pytest_httpx-0.35.0-py3-none-any.whl (19 kB)
Using cached pytest_asyncio-1.2.0-py3-none-any.whl (15 kB)
Using cached pytest_cov-7.0.0-py3-none-any.whl (22 kB)
Using cached pytest_xdist-3.8.0-py3-none-any.whl (46 kB)
Using cached gunicorn-23.0.0-py3-none-any.whl (85 kB)
Using cached annotated_types-0.7.0-py3-none-any.whl (13 kB)
Using cached certifi-2025.8.3-py3-none-any.whl (161 kB)
Using cached click-8.3.0-py3-none-any.whl (107 kB)
Using cached coverage-7.10.7-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (252 kB)
Using cached execnet-2.1.1-py3-none-any.whl (40 kB)
Using cached h11-0.16.0-py3-none-any.whl (37 kB)
Using cached iniconfig-2.1.0-py3-none-any.whl (6.0 kB)
Using cached packaging-25.0-py3-none-any.whl (66 kB)
Using cached pygments-2.19.2-py3-none-any.whl (1.2 MB)
Using cached sniffio-1.3.1-py3-none-any.whl (10 kB)
Using cached typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Using cached typing_inspection-0.4.1-py3-none-any.whl (14 kB)
Installing collected packages: urllib3, typing-extensions, sniffio, PyJWT, pygments, pluggy, packaging, iniconfig, idna, h11, execnet, coverage, click, charset_normalizer, certifi, annotated-types, uvicorn, typing-inspection, requests, pytest, pydantic-core, httpcore, gunicorn, anyio, starlette, pytest-xdist, pytest-cov, pytest-asyncio, pydantic, httpx, pytest-httpx, fastapi
Successfully installed PyJWT-2.10.1 annotated-types-0.7.0 anyio-4.11.0 certifi-2025.8.3 charset_normalizer-3.4.3 click-8.3.0 coverage-7.10.7 execnet-2.1.1 fastapi-0.117.1 gunicorn-23.0.0 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.10 iniconfig-2.1.0 packaging-25.0 pluggy-1.6.0 pydantic-2.11.9 pydantic-core-2.33.2 pygments-2.19.2 pytest-8.4.2 pytest-asyncio-1.2.0 pytest-cov-7.0.0 pytest-httpx-0.35.0 pytest-xdist-3.8.0 requests-2.32.5 sniffio-1.3.1 starlette-0.48.0 typing-extensions-4.15.0 typing-inspection-0.4.1 urllib3-2.5.0 uvicorn-0.37.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
$ echo "Running automated test suite..."
Running automated test suite...
$ pytest --maxfail=1 --disable-warnings --cov=services --cov-report=term --cov-report=xml --junitxml=tests/reports/junit.xml
============================= test session starts ==============================
platform linux -- Python 3.12.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /builds/Jayaraj-s/integrated-test-assign
plugins: cov-7.0.0, httpx-0.35.0, xdist-3.8.0, anyio-4.11.0, asyncio-1.2.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 62 items
tests/test_auth.py ........................                              [ 38%]
tests/test_performance.py ...                                            [ 43%]
tests/test_storage_api.py ...................................            [100%]
- generated xml file: /builds/Jayaraj-s/integrated-test-assign/tests/reports/junit.xml -
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.11-final-0 _______________
Name                          Stmts   Miss  Cover
-------------------------------------------------
services/__init__.py              0      0   100%
services/auth_service.py         55      0   100%
services/storage_service.py      41      0   100%
-------------------------------------------------
TOTAL                            96      0   100%
Coverage XML written to file coverage.xml
======================== 62 passed, 1 warning in 4.56s =========================
Saving cache for successful job
00:02
Creating cache default-protected...
.cache/pip: found 593 matching artifact files and directories 
Uploading cache.zip to https://storage.googleapis.com/gitlab-com-runners-cache/project/74811778/default-protected 
Created cache
Uploading artifacts for successful job
00:02
Uploading artifacts...
tests/reports/: found 2 matching artifact files and directories 
coverage.xml: found 1 matching artifact files and directories 
WARNING: htmlcov/: no matching files. Ensure that the artifact path is relative to the working directory (/builds/Jayaraj-s/integrated-test-assign) 
Uploading artifacts as "archive" to coordinator... 201 Created  correlation_id=c8691613530f48c89677f0a66308d92c id=11521669399 responseStatus=201 Created token=6a_xxWp59
Uploading artifacts...
tests/reports/junit.xml: found 1 matching artifact files and directories 
Uploading artifacts as "junit" to coordinator... 201 Created  correlation_id=a515cf58ed064901ab79768e4c2e7438 id=11521669399 responseStatus=201 Created token=6a_xxWp59
Cleaning up project directory and file based variables
00:01
Job succeeded
```
