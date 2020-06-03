FROM ubuntu:16.04


RUN apt-get update
RUN apt-get -y install apache2
RUN apt-get -y install python3 python3-pip

#load apache cgi module
RUN a2enmod cgi

#enable cgi in the website root
RUN echo "                       \n \
<Directory /var/www/html>        \n \
   Options +ExecCGI              \n \
   AddHandler cgi-script .py     \n \
   DirectoryIndex db_parser.py       \n \
</Directory>                     \n \
" >> /etc/apache2/apache2.conf

RUN service apache2 restart

COPY ./scripts/db_parser.py /var/www/html
COPY ./requirements.txt /var/www/html
COPY ./data /var/www/data

RUN chmod -R u+rwx,g+x,o+x /var/www/html
RUN chmod -R u+rwx,g+x,o+x /var/www/data

RUN ln -sf /usr/bin/python3 /usr/local/bin/python
RUN pip3 install -r /var/www/html/requirements.txt

EXPOSE 80


ENTRYPOINT /usr/sbin/apache2ctl -D FOREGROUND