# RESTful API 서버

- Date : 2024.10.10 ~ 2024.10.14
- Author : Hyunyoun Jo <chochyjj@gmail.com>
- Language : Python (3.12.7)
- Framework: Django

---

## 개요

 사출기 관리 시스템을 위한 RESTful API를 설계하고 구현한다.

## 요구사항

- 데이터 저장을 위해 PostgreSQL 데이터베이스를 사용한다.
- API는 JSON 형식으로 데이터를 주고받아야 한다.
- HTTP 상태 코드를 적절히 사용해야 한다.

## 기능 설명

- API 문서 URI : `api/swagger/` 또는 `api/docs/`
- 기능
  - 사용자 등록  
    - URI : `/api/sign-up/`  
    - METHOD : POST  
    - DESCRIPTION : 사용자를 시스템에 등록한다.  
    - REQUEST  
      - BODY

        ```json
        {
          "username": "string",
          "password": "string",
          "first_name": "string",
          "last_name": "string",
          "email": "user2@example.com"
        }
        ```

      - RESPONSE

  - 사용자 로그인  
    - URI : `/api/sign-in/`  
    - METHOD : POST  
    - DESCRIPTION : 시스템에 등록된 사용자가 로그인할 수 있다.  
    - REQUEST  
      - BODY

        ```json
        {
          "username": "string",
          "password": "string"
        }
        ```

      - RESPONSE

  - 사출기 추가  
    - URI : `/api/machines/`  
    - METHOD : POST  
    - DESCRIPTION : 인증된 사용자가 새로운 사출기를 추가할 수 있다.  
    - REQUEST
      - BODY

        ```json
        {
          "name": "string",
          "location": "string",
          "status": 0,
          "owner_id": 2
        }
        ```

      - RESPONSE

  - 사출기 조회  
    - URI : `/api/machines/<int: pk>/`  
    - METHOD : GET  
    - DESCRIPTION : 인증된 사용자는 특정 사출기의 정보를 조회할 수 있다.  
    - REQUEST  
      - QUERY STRING
    - RESPONSE

  - 사출기 목록 조회
    - URI : `/api/machines/`  
    - METHOD : GET  
    - DESCRIPTION : 인증된 사용자는 모든 사출기의 목록을 조회할 수 있다.  
    - REQUEST  
      - QUERY STRING
      - PAGINATION
    - RESPONSE

  - 사출기 수정  
    - URI : `/api/machines/<int: pk>/`  
    - METHOD : PUT  
    - DESCRIPTION : 인증된 사용자는 자신이 추가한 사출기의 정보를 수정할 수 있다.  
    - REQUEST  
      - BODY

        ```json
        {
          "name": "string",
          "location": "string",
          "status": 0,
          "owner_id": 2
        }
        ```

    - RESPONSE
    - INFO
      - 자신이 추가하지 않은 사출기일 경우, PermissionDenied

  - 사출기 삭제  
    - URI : `/api/machines/<int: pk>/`  
    - METHOD : DELETE  
    - DESCRIPTION : 인증된 사용자는 자신이 추가한 사출기를 삭제할 수 있다.  
    - REQUEST
    - RESPONSE  
    - INFO
      - 자신이 추가하지 않은 사출기일 경우, PermissionDenied

  - 사출기 작업 시작  
    - URI : `/api/machines/<int: pk>/operation/`  
    - METHOD : POST  
    - DESCRIPTION : 인증된 사용자는 사출기 작업을 시작할 수 있다.  
    - REQUEST  
      - BODY

        ```json
        {
          "command" : "START"
        }
        ```

    - INFO
      - 비동기 구현

  - 사출기 작업 중지  
    - URI : `/api/machines/<int: pk>/operation/`  
    - METHOD : POST  
    - DESCRIPTION : 인증된 사용자는 사출기 작업을 중지할 수 있다.  
    - REQUEST  
      - BODY

        ```json
        {
          "command" : "STOP"
        }
        ```

    - INFO
      - 비동기 구현

  - 사출기 작업 기록 조회  
    - URI : `/api/machines/history/`
    - METHOD : GET  
    - DESCRIPTION : 인증된 사용자는 자신의 사출기 작업 기록을 조회할 수 있다.  
    - INFO
      - 자신이 추가하지 않은 사출기일 경우, PermissionDenied  

  - 사출기의 작업 기록 조회  
    - URI : `/api/machines/<int:pk>/history/`
    - METHOD : GET  
    - DESCRIPTION : 인증된 사용자는 특정 사출기 작업 기록을 조회할 수 있다.
    - INFO
      - 자신이 추가하지 않은 사출기일 경우, PermissionDenied  

## 데이터 설계  

### Auth

- 사용자의 계정을 관리한다.
- Fields
  - id : UID
  - `[필수]` password : 비밀번호 (pbkdf2 sha256)
  - last_login : 마지막 로그인한 날짜
  - `[필수][Unique]` username : ID
  - `[필수][Unique]` email : E-mail 주소
  - is_staff : 관리자 여부
  - is_active : 계정의 활성화 여부
  - is_superuser : admin 여부
  - `[필수]`first_name : 이름
  - `[필수]`last_name: 성
  - date_joined : 가입일

|id|password|last_login|username|email|is_staff|is_active|is_superuser|first_name|last_name|date_joined|
|--|--------|----------|--------|-----|--------|---------|------------|----------|---------|-----------|
|1|pbkdf2_sha256$870000$j8Ynv4lMbqIcf8eKI4wTIn$Y9G0ULru6AOeRNkXlOyF5hzuwkED/Bcv872nHAD87qM=||admin|<abcd@abcd.com>|true|true|true|admin|jo|2024-10-13 00:49:38.385 +0900|
|3|pbkdf2_sha256$870000$XHNNCuta2D12z5JA1eTzUD$cbQ+6jO90DhbYN+TeqdxI1cxQU3WBh99HxhHppiNPsg=||string1|<user1@example.com>|false|true|false|string|string|2024-10-13 02:04:10.569 +0900|
|2|pbkdf2_sha256$870000$Cl1YMSSfjk2Z3tHD2tt9I9$UexVONA3YOlxc1pVrW+z5hnWziqQ1ZyHasFFle38XR4=|2024-10-13 13:32:44.227 +0900|string|<user@example.com>|false|true|false|string|string|2024-10-13 00:50:45.936 +0900|

### InjectionMoldingMachines  

- 사출기의 정보를 관리한다.
- 각 사출기는 id, name, location, status, owner_id를 포함해야 한다.  
- Fields
  - id : UID
  - `[필수]` name : 사출기의 이름
  - `[필수]` location : 사출기가 위치한 장소
  - `[필수]` status : 사출기의 상태
    > - status [class MachineStatus](./defines/data_status.py)
    >   - POWEROFF = 1  # 전원 꺼짐
    >   - READY = 2  # 전원이 켜졌으나 작업이 되고 있지 않음.
    >   - PAUSE = 3  # 작업중 일시중단된 상태
    >   - RUNNING = 4  # 작업중
    >   - ERROR = 5  # 작업중 원인 불명의 원인으로 문제 발생함
  - `[필수]` owner_id : 사출기의 소유자
  - created_at : 생성일
  - updated_at : 수정일

|id|name|location|status|owner_id|created_at|updated_at|  
|--|----|--------|------|--------|----------|----------|  
|2|string1|string1|1|2|2024-10-13 00:52:20.739 +0900|2024-10-13 00:52:20.739 +0900|  
|3|string2|string2|1|2|2024-10-13 00:52:27.818 +0900|2024-10-13 00:52:27.818 +0900|  
|4|string3|string3|1|2|2024-10-13 00:52:35.684 +0900|2024-10-13 00:52:35.684 +0900|  
|5|string4|string4|1|2|2024-10-13 00:52:41.437 +0900|2024-10-13 00:52:41.437 +0900|  
|6|string5|string5|1|2|2024-10-13 00:52:46.243 +0900|2024-10-13 00:52:46.243 +0900|  
|7|string6|string6|1|2|2024-10-13 00:52:51.910 +0900|2024-10-13 00:52:51.910 +0900|  
|8|string7|string7|1|2|2024-10-13 00:52:56.777 +0900|2024-10-13 00:52:56.777 +0900|  
|9|string8|string8|1|2|2024-10-13 00:53:02.208 +0900|2024-10-13 00:53:02.208 +0900|  
|10|string9|string9|1|2|2024-10-13 00:53:06.922 +0900|2024-10-13 00:53:06.922 +0900|  
|11|string10|string10|1|2|2024-10-13 00:53:16.284 +0900|2024-10-13 00:53:16.284 +0900|  

### MachinesHistory

- 각 사출기의 작업 목록을 관리한다.
- Fields
  - id : UID
  - `[필수]` request_datetime : 작업을 요청한 시각
  - `[필수]` command : 명령 타입
    > - command [class OperationCommands](./defines/operation_commands.py)
    >   - START = auto()  # 동작 시작
    >   - STOP = auto()  # 동작 중단
  - `[필수]` worker : 명령을 한 사용자
  - `[필수]` machine_id : 사용자가 명령한 사출기의 ID
  - `[필수]` machine_owner_id : 사용자가 명령한 사출기의 소유자
  - `[필수]` result : 요청에 대한 결과
    > - result  [class OperationResult](./defines/data_status.py)
    >   - SUCCESS = 1
    >   - REMOTEFAILED = 2
    >   - INTERNALFAILED = 3
    >   - PENDING = 4
  - created_at : 생성일  

|id|request_datetime|command|worker|machine_id|machine_owner_id|created_at|result|
|--|----------------|-------|------|----------|----------------|----------|------|

## 프로그램 흐름도: 주요 기능과 그들 간의 상호작용을 도표로 표현합니다

## 보안 요구사항  

- 사용자 인증을 위해 JWT(JSON Web Token)를 사용한다.
  - 인증된 사용자가 사출기에 대한 CRUD를 수행할 수 있다.
  - 인증된 사용자가 사출기에 대한 작업을 시작/중지할 수 있다.
  - 인증된 사용자가 사출기의 작업 기록을 조회할 수 있다.

## 성능 요구사항

- 비동기 작업 처리를 위해 Celery와 Redis를 사용합니다.

## 기타  

### Usage

- 시스템 구동

  ```bash
  poetry run python manage.py runserver 0.0.0.0:8000
  ```

- celery 구동

  ```bash
  celery -A config worker -l INFO --autoscale 2,5
  ```

### 설정

- Django의 설정 경로는 `config/settings/`
  - `settings.py`에 있던 설정을 분리하여 각각의 파일로 만들었으며 `__init__.py`에서 해당 파일에 설정된 변수값들을 불어와서 선언함.
- 환경변수에 등록된 `MODE`에 따라서 settings의 DEBUG, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS의 입력값이 변동됨.
  - 환경변수는 Docker를 Build할 때 선언됨.
  - MODE의 종류
    - DEV : 개발
    - RELEASE : 실운영

### 개발환경

- Linter & Formatter : [ruff](https://docs.astral.sh/ruff/#ruff)  
  - An extremely fast Python linter and code formatter, written in Rust.  

### 계정  

- Super Admin
  - ID : admin
  - PW : 1qaz2wsx

### 폴더 구조

```bash
proj-injection
├─.vscode
├─apps
│  ├─accounts
│  │  ├─migrations
│  │  ├─models
│  │  ├─serializers
│  │  ├─tasks
│  │  ├─tests
│  │  ├─views
│  └─machines
│      ├─migrations
│      ├─models
│      ├─serializers
│      ├─tasks
│      ├─tests
│      └─views
├─base_modules
│  ├─exception_handler
│  ├─middleware_handler
│  ├─response_handler 
│  └─swagger_schema_view
├─config
│  └─settings
├─defines
├─docs
├─fixtures
├─logs
│  ├─celery
│  ├─error
│  ├─server
│  └─system
├─media
├─pids
├─static
└─tests
```
