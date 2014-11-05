Name:           analytics-server
Version:        0.1.0
Release:        1
Summary:        Server for the XoAnalytics Android tool

License:        GPLv2+
URL:            https://github.com/tchx84/analytics-server
Source0:        analytics-server-0.1.0.tar

Requires:       python >= 2.7, python-tornado >= 2.2.1, openssl >= 1.0.1, mysql-server >= 5.5, MySQL-python >= 1.2.3 

BuildArch:      noarch

#GitUrl: https://github.com/tchx84/analytics-server.git
#GitBranch: master
#GitCommit: 99e6a82f72741ef3d9cbb4c7cf3644cd27955741

%description
Server for the XoAnalytics Apps usage tracking tool for Android

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/opt/analytics/
cp -r analytics migrations misc server.py $RPM_BUILD_ROOT/opt/analytics/

mkdir $RPM_BUILD_ROOT/opt/analytics/etc
cp etc/analytics.cfg.example $RPM_BUILD_ROOT/opt/analytics/etc/analytics.cfg.example

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/
cp etc/analytics.service.example $RPM_BUILD_ROOT/%{_sysconfdir}/systemd/system/analytics.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
exists=$(getent passwd analytics > /dev/null)
if [ $? = "0" -a -z "$exists" ]; then
    echo "Using existing user"
else
    useradd --user-group \
            --shell /sbin/nologin \
            --comment "analytics server" \
            analytics
    echo "Created new user"
fi

%post
if [ ! -f /opt/analytics/etc/analytics.cfg ]; then
    cp /opt/analytics/etc/analytics.cfg.example /opt/analytics/etc/analytics.cfg
    echo "Created new configuration file"
else
    echo "Using existing configuration file"
fi

if [ ! -f /opt/analytics/etc/analytics.crt ] || [ ! -f /opt/analytics/etc/analytics.key ]; then
    /opt/analytics/misc/generate.sh > /dev/null 2>&1
    mv localhost.crt.example /opt/analytics/etc/analytics.crt
    mv localhost.key.example /opt/analytics/etc/analytics.key
    echo "Created new certificate and key files"
else
    echo "Using existing certificate and key files"
fi

cd /opt/analytics/migrations/
db-migrate

%files
%defattr(-,root,root)
%attr(0754, analytics, analytics) /opt/analytics/server.py
%attr(0754, root, root) /opt/analytics/misc/generate.sh
/opt/analytics/analytics/handlers.py
/opt/analytics/analytics/__init__.py
/opt/analytics/analytics/errors.py
/opt/analytics/analytics/report.py
/opt/analytics/analytics/decorators.py
/opt/analytics/analytics/datastore.py
/opt/analytics/etc/analytics.cfg.example
/opt/analytics/migrations/20141014092823_create_table_times.migration
/opt/analytics/migrations/simple-db-migrate.conf
/opt/analytics/misc/generate.sh
/opt/analytics/misc/init.sql
%{_sysconfdir}/systemd/system/analytics.service

%changelog
* Tue Oct 14 2014 Martin Abente Lahaye <tch@sugarlabs.org>
- Initial package
