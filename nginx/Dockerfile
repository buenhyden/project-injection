FROM nginx

# COPY ./nginx/config/nginx.conf /etc/nginx/conf.d/nginx.conf
RUN mkdir /static/
COPY ./nginx/config/nginx.conf /etc/nginx/conf.d/default.conf
COPY ./proj-injection/static/ /static/
RUN chmod 777 /static/ -R
ENTRYPOINT ["nginx", "-g", "daemon off;"]