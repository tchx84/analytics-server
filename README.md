analytics-server
================
This is the server for OLPC-AU analytics suite.

Setup
----

0. Install server dependencies:

    ```
    $yum install git openssl mysql-server python python-pip MySQL-python tornado
    $pip install db-migrate
    ```

1. Create analytics user:

    ```
    $useradd --user-group --shell /sbin/nologin --comment "analytics server" analytics
    ```

2. Get the server bits:

    ```
    $cd /opt/
    $git clone https://github.com/tchx84/analytics-server.git analytics
    $cd analytics
    $chown analytics:analytics server.py
    ```

3. Create the SSL certificates (make sure to assign a Common Name):

    ```
    $openssl req -newkey rsa:2048 -x509 -days 3650 -nodes -out analytics.crt -keyout analytics.key
    $mv analytics.key analytics.crt etc/
    ```

4. Create configuration file:

    ```
    $cp etc/analytics.cfg.example etc/analytics.cfg
    $vim etc/analytics.cfg
    ```

5. Create the database:

    ```
    $service mysqld start
    $mysql -u root -p < misc/init.sql
    $cd migrations/
    $db-migrate 
    ```

6. Enable server service:

   ```
   $cd /opt/analytics/
   $cp etc/analytics.service.example /etc/systemd/system/analytics.service
   $service analytics start
   ```
