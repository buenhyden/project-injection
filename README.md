# Project

- Date : 2024.10.10 ~ 2024.10.14
- Author : Hyunyoun Jo <chochyjj@gmail.com>

---

## 개요

 사출기 관리 시스템을 설계하고 구현한다.

## 요구사항

- 각 사출기는 id, name, location, status, owner_id를 포함해야 합니다.
- 데이터 저장을 위해 PostgreSQL 데이터베이스를 사용합니다.
- 사용자 인증을 위해 JWT(JSON Web Token)를 사용합니다.
- 비동기 작업 처리를 위해 Celery와 Redis를 사용합니다.
- API는 JSON 형식으로 데이터를 주고받아야 합니다.
- HTTP 상태 코드를 적절히 사용해야 합니다.

## 시스템 아키텍처

![시스템 구조도(DEV)](./assets/system-architecture(dev).jpg)

![시스템 구조도(RELEASE)](./assets/system-architecture(release).jpg)

### 구성요소

#### PostgreSQL

- object-relational database management system (ORDBMS).
- RESTful API Server에서 Database로 사용한다.
- 유저 정보
  - ID : postgres
  - PW : NbpqVlRL0ugfoD9

#### REDIS

- Redis works well for rapid transport of small messages.  
- Redis is a super fast K/V store, making it very efficient for fetching the results of a task call.
- 유저 정보  
  - PW : xtM6wEiKg6J4Rdc

#### Celery

- 분산 메시지 전달을 기반으로 동작하는 비동기 작업 큐(Asynchronous Task/Job Queue).  
- 사용자에게 즉각적인 반응을 보여줄 필요가 없는 작업들로 인해 사용자가 느끼는 Delay를 최소하 화기 위해 사용 된다

#### RESTful API Server

- 요청을 처리하는 API 서버.

## 기능 설명

- swagger : `/api/swagger/`
- doc : `/api/docs/`  
[RESTful API Server](./proj-injection/README.md#기능-설명)

## 데이터 설계  

[데이터 설계](./proj-injection/README.md#데이터-설계)

## 보안 요구사항  

- 사용자 인증을 위해 JWT(JSON Web Token)를 사용한다.
  - 인증된 사용자가 사출기에 대한 CRUD를 수행할 수 있다.
  - 인증된 사용자가 사출기에 대한 작업을 시작/중지할 수 있다.
  - 인증된 사용자가 사출기의 작업 기록을 조회할 수 있다.
- JWT
  - Access Token Lifetime : 30min
  - Refresh Token Lifetime : 1days
  - AUTH_HEADER_TYPES : Bearer
  - AUTH_HEADER_NAME : HTTP_AUTHORIZATION

## 기타  

### Usage

Build는 `config-injection/Dockerfile`로 이루어진다.

#### 개발 환경 세팅

1. Build

    ```bash
    docker compose -f .\docker-compose.project.dev.yml build --no-cache
    ```

2. 실행

    ````bash
    docker compose -f docker-compose.project.dev.yml up -d
    ````

#### 실운영

1. Build

    ```bash
    docker compose -f .\docker-compose.project.release.yml build --no-cache
    ```

2. 실행

    ````bash
    docker compose -f docker-compose.project.release.yml up -d
    ````

### 폴더 구조  

- assets : README.md의 리소스  
- config-injection : 개발 환경의 docker를 세팅하기 위해 필요한 파일  
- databases : 개발 환경에서 docker의 container가 올라가 있는 postgresql과 redis를 마운트하기 위한 폴더.  
- nginx : release에서 사용할 nginx build용 Dockerfile과 conf 파일이 저장되어 있는 폴더.  
- proj-injection : 작업내용.

```bash
project-injection
├─assets
├─config-injection
│  └─.vscode
├─databases
│  ├─postgres
│  └─redis
├─nginx
│  └─config
└─proj-injection    
    ├─.vscode
    ├─apps
    │  ├─accounts
    │  │  ├─migrations
    │  │  ├─models
    │  │  ├─serializers
    │  │  ├─tasks
    │  │  ├─tests
    │  │  └─views
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
