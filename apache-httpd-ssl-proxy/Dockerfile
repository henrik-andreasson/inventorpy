FROM httpd:2.4

COPY cert.pem /usr/local/apache2/conf/
COPY key.pem /usr/local/apache2/conf/
COPY ca.pem /usr/local/apache2/conf/
#COPY ca-chain.pem /usr/local/apache2/conf/
COPY ssl-proxy-host.conf /usr/local/apache2/conf/
RUN echo "Include conf/ssl-proxy-host.conf" >> /usr/local/apache2/conf/httpd.conf
