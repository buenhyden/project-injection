FROM python:3.12-slim AS python3.12_base
LABEL version="0.1" creator="chochyjj@gmail.com" description="Python 3.12"

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates systemd openssh-server default-libmysqlclient-dev build-essential libpq-dev apt-utils gcc g++ git git-flow wget curl gfortran cmake pkg-config locales netcat-traditional\
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
    && apt-get clean \
    && update-ca-certificates \
    && localedef -i ko_KR -c -f UTF-8 -A /usr/share/locale/locale.alias ko_KR.UTF-8
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
RUN systemctl enable ssh
# Project
RUN mkdir /project/
WORKDIR /project/

FROM python3.12_base AS dev_project
LABEL version="0.1" creator="chochyjj@gmail.com" description="Project Injection Dev"
# 로컬에 있는 pyproject.toml, poetry.lock 파일을 컨테이너로 복사
ENV MODE=DEV
# COPY ./.ssh /root/.ssh
# RUN git config --global core.editor "code --wait"
# RUN git config --global user.email "chochyjj@gmail.com"
# RUN git config --global user.name "Hyunyoun Jo"
# RUN chmod 600 /root/.ssh/id_rsa
# RUN chmod 600 /root/.ssh/id_rsa.pub
COPY ./config-injection/poetry.lock ./config-injection/pyproject.toml /project/
# Poetry 설치
RUN pip install -U poetry
# Poetry를 이용하여 의존성 설치 
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction    
COPY ./config-injection/README.md README.md
COPY ./config-injection/.vscode .vscode
COPY ./config-injection/.pre-commit-config.yaml .
COPY ./config-injection/.gitignore .gitignore
COPY ./config-injection/gitmessage.txt gitmessage.txt
COPY ./config-injection/zsh-in-docker.sh .
RUN chmod 755 /project/zsh-in-docker.sh
RUN /project/zsh-in-docker.sh \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -p https://github.com/zsh-users/zsh-history-substring-search \
    -p https://github.com/zsh-users/zsh-syntax-highlighting \
    -p 'history-substring-search' \
    -a 'bindkey "\$terminfo[kcuu1]" history-substring-search-up' \
    -a 'bindkey "\$terminfo[kcud1]" history-substring-search-down'
RUN mkdir ~/.oh-my-zsh/completions
RUN poetry completions zsh  > ~/.oh-my-zsh/completions/_poetry    
RUN mkdir /project/pids
RUN mkdir /project/logs
RUN mkdir /project/celery
RUN mkdir /project/apps
RUN mkdir /project/apps/accounts
RUN mkdir /project/apps/machines

FROM python3.12_base AS release_project
LABEL version="0.1" creator="chochyjj@gmail.com" description="Project Injection release"
ENV MODE=RELEASE
ENV DEFAULT_PYTHON_DJANGO_PORT=8000
ENV REDIS_PORT=6379
ENV REDIS_HOSTNAME=release-proj-redis
# ENV REDIS_PASSWORD=xtM6wEiKg6J4Rdc
ENV REDIS_PASSWORD=xtM6wEiKg6J4Rdc
ENV RDBMS_ROOT_PASSWORD=NbpqVlRL0ugfoD9
ENV POSTGRES_HOSTNAME=release-proj-postgres
ENV POSTGRES_PORT=5432
# ENV DEFAULT_USERNAME=hyden
ENV DEFAULT_USERNAME=postgres
ENV POSTGRES_PASSWORD=NbpqVlRL0ugfoD9

COPY ./proj-injection/ .
RUN rm .history/ -rf
RUN rm ./logs/ -rf
RUN rm ./pids/ -rf
RUN mkdir /project/pids
RUN mkdir /project/logs
# Poetry 설치
RUN pip install -U poetry
# Poetry를 이용하여 의존성 설치 
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction
RUN chmod +x /project/entrypoint.sh
ENTRYPOINT ["/project/entrypoint.sh"]

FROM python3.12_base AS release_celery
LABEL version="0.1" creator="chochyjj@gmail.com" description="Project Injection celery"
ENV MODE=RELEASE
ENV DEFAULT_PYTHON_DJANGO_PORT=8000
ENV REDIS_PORT=6379
ENV REDIS_HOSTNAME=release-proj-redis
# ENV REDIS_PASSWORD=xtM6wEiKg6J4Rdc
ENV REDIS_PASSWORD=xtM6wEiKg6J4Rdc
ENV RDBMS_ROOT_PASSWORD=NbpqVlRL0ugfoD9
ENV POSTGRES_HOSTNAME=release-proj-postgres
ENV POSTGRES_PORT=5432
# ENV DEFAULT_USERNAME=hyden
ENV DEFAULT_USERNAME=postgres
ENV POSTGRES_PASSWORD=NbpqVlRL0ugfoD9

COPY ./proj-injection/ .
RUN rm .history/ -rf
RUN rm ./logs/ -rf
RUN rm ./pids/ -rf
RUN mkdir /project/pids
RUN mkdir /project/logs
# Poetry 설치
RUN pip install -U poetry
# Poetry를 이용하여 의존성 설치 
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction
