#FROM tutum/nginx
#RUN rm /etc/nginx/sites-enabled/default
#ADD sites-enabled/ /etc/nginx/sites-enabled

FROM tutum/nginx
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/django_project /etc/nginx/conf.d/
ADD sites-enabled/ /etc/nginx/sites-enabled
