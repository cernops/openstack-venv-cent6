%global python_name ceilometer
%global daemon_prefix openstack-ceilometer
%global os_version 2015.1.1
%global os_release 1
%global _without_doc 1
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

%if ! 0%{?overwrite_configs}
%global configfile %config(noreplace)
%else
%global configfile %verify(mode)
%endif

Name:             openstack-ceilometer
Version:          %{os_version}
Release:          %{os_release}%{?dist}
Summary:          OpenStack measurement collection service

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Ceilometer
Source0:          %{python_name}-%{os_version}.tar.gz

%if ! (0%{?rhel} > 6)
Source10:         openstack-ceilometer-api.init
Source11:         openstack-ceilometer-collector.init
Source12:         openstack-ceilometer-compute.init
Source13:         openstack-ceilometer-central.init
Source14:         openstack-ceilometer-alarm-notifier.init
Source15:         openstack-ceilometer-alarm-evaluator.init
%else
Source10:         openstack-ceilometer-api.service
Source11:         openstack-ceilometer-collector.service
Source12:         openstack-ceilometer-compute.service
Source13:         openstack-ceilometer-central.service
Source14:         openstack-ceilometer-alarm-notifier.service
Source15:         openstack-ceilometer-alarm-evaluator.service
%endif
#if $newer_than_eq('2014.1')
%if ! (0%{?rhel} > 6)
Source16:         openstack-ceilometer-notification.init
%else
Source16:         openstack-ceilometer-notification.service
%endif
#end if
#if $newer_than_eq('2014.2')
%if ! (0%{?rhel} > 6)
Source17:         openstack-ceilometer-ipmi.init
%else
Source17:         openstack-ceilometer-ipmi.service
%endif
#end if
#if $newer_than_eq('2015.1')
%if ! (0%{?rhel} > 6)
Source19:         openstack-ceilometer-polling.init
%else
Source19:         openstack-ceilometer-polling.service
%endif
#end if

Source20:          ceilometer-dist.conf
Source21:          ceilometer.conf
Source22:          ceilometer.logrotate
Source23:          policy.json
Source24:          pipeline.yaml

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:        noarch

Requires:         %{name}-common = %{version}-%{release}
Requires:         %{name}-compute = %{version}-%{release}
Requires:         %{name}-central = %{version}-%{release}
Requires:         %{name}-collector = %{version}-%{release}
Requires:         %{name}-api = %{version}-%{release}
Requires:         %{name}-alarm = %{version}-%{release}
Requires:         %{name}-notification = %{version}-%{release}
Requires:         %{name}-ipmi = %{version}-%{release}
Requires:         %{name}-polling = %{version}-%{release}

%description
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

%package -n       python-ceilometer
Summary:          OpenStack ceilometer python libraries
Group:            Applications/System

%description -n   python-ceilometer
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer python library.

%package common
Summary:          Components common to all OpenStack ceilometer services
Group:            Applications/System

Requires:         python-ceilometer = %{version}-%{release}

%if 0%{?rhel} && 0%{?rhel} <= 6
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
%else
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
%endif

Requires(pre):    shadow-utils

%description common
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains components common to all OpenStack
ceilometer services.

%package compute
Summary:          OpenStack ceilometer compute agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description compute
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer agent for
running on OpenStack compute nodes.

%package central
Summary:          OpenStack ceilometer central agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description central
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the central ceilometer agent.

%package collector
Summary:          OpenStack ceilometer collector agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description collector
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer collector agent.

%package api
Summary:          OpenStack ceilometer API service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description api
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer API service.

%package alarm
Summary:          OpenStack ceilometer alarm services
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description alarm
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer alarm notification
and evaluation services.

#if $newer_than_eq('2014.1')
%package notification
Summary:          OpenStack ceilometer notifier services
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description notification
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer alarm notification
and evaluation services.
#end if

#if $newer_than_eq('2014.2')
%package ipmi
Summary:          OpenStack ceilometer ipmi agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description ipmi
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ipmi agent to be run on OpenStack
nodes from which IPMI sensor data is to be collected directly,
by-passing Ironic's management of baremetal.
#end if

#if $newer_than_eq('2015.1')
%package polling
Summary:          OpenStack ceilometer polling agent
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description polling
Ceilometer aims to deliver a unique point of contact for billing systems to
aquire all counters they need to establish customer billing, across all
current and future OpenStack components. The delivery of counters must
be tracable and auditable, the counters must be easily extensible to support
new projects, and agents doing data collections should be
independent of the overall system.

This package contains the polling service.
#end if

%prep
%setup -q -n %{python_name}-%{os_version}

%install

install -p -D -m 644 %{python_name}-%{os_version}-%{os_release}-venv.tar.gz %{buildroot}/opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{os_release}-venv.tar.gz
#make sure the /usr/share/ceilometer dirs exist
mkdir -p %{buildroot}/usr/share/ceilometer

%if 0%{?with_doc}
#raw
export PYTHONPATH="$PWD:$PYTHONPATH"
pushd doc
sphinx-build -b html source build/html
popd
#end raw
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/ceilometer

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer
#if $older_than('2014.2')
install -p -D -m 640 %{SOURCE20} %{buildroot}%{_datadir}/ceilometer/ceilometer-dist.conf
install -p -D -m 640 %{SOURCE21} %{buildroot}%{_sysconfdir}/ceilometer/ceilometer.conf

install -p -D -m 640 %{SOURCE23} %{buildroot}%{_sysconfdir}/ceilometer/policy.json
install -p -D -m 640 %{SOURCE24} %{buildroot}%{_sysconfdir}/ceilometer/pipeline.yaml
#end if

%if ! (0%{?rhel} > 6)
# Install initscripts for services
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-collector
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-central
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{name}-alarm-notifier
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{name}-alarm-evaluator
%else
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-collector.service
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-compute.service
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-central.service
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_unitdir}/%{name}-alarm-notifier.service
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_unitdir}/%{name}-alarm-evaluator.service
%endif
#if $newer_than_eq('2014.1')
%if ! (0%{?rhel} > 6)
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{name}-notification
%else
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_unitdir}/%{name}-notification.service
%endif
#end if
#if $newer_than_eq('2014.2')
%if ! (0%{?rhel} > 6)
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{name}-ipmi
%else
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_unitdir}/%{name}-ipmi.service
%endif
#end if
#if $newer_than_eq('2015.1')
%if ! (0%{?rhel} > 6)
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/%{name}-polling
%else
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_unitdir}/%{name}-polling.service
%endif
#end if
#Fix for bin path for central and compute
%if ! (0%{?rhel} > 6)
sed -i "s#/usr/bin/ceilometer-compute#/usr/bin/ceilometer-agent-compute#" %{buildroot}%{_initrddir}/%{name}-compute
sed -i "s#/usr/bin/ceilometer-central#/usr/bin/ceilometer-agent-central#" %{buildroot}%{_initrddir}/%{name}-central
%else
sed -i "s#/usr/bin/ceilometer-compute#/usr/bin/ceilometer-agent-compute#" %{buildroot}%{_unitdir}/%{name}-compute.service
sed -i "s#/usr/bin/ceilometer-central#/usr/bin/ceilometer-agent-central#" %{buildroot}%{_unitdir}/%{name}-central.service
%endif
#if $newer_than_eq('2014.1')
%if ! (0%{?rhel} > 6)
sed -i "s#/usr/bin/ceilometer-notification#/usr/bin/ceilometer-agent-notification#" %{buildroot}%{_initrddir}/%{name}-notification
%else
sed -i "s#/usr/bin/ceilometer-notification#/usr/bin/ceilometer-agent-notification#" %{buildroot}%{_unitdir}/%{name}-notification.service
%endif
#end if

# Install logrotate
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/ceilometer

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/ceilometer-debug
rm -fr %{buildroot}%{python_sitelib}/tests/
rm -fr %{buildroot}%{python_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/ceilometer/README*

%pre common
getent group ceilometer >/dev/null || groupadd -r ceilometer --gid 166
if ! getent passwd ceilometer >/dev/null; then
  # Id reservation request: https://bugzilla.redhat.com/923891
  useradd -u 166 -r -g ceilometer -G ceilometer,nobody -d %{_sharedstatedir}/ceilometer -s /sbin/nologin -c "OpenStack ceilometer Daemons" ceilometer
fi
exit 0


%post compute
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-compute
fi
%else
%systemd_post %{name}-compute.service
%endif

%post collector
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-collector
fi
%else
%systemd_post %{name}-collector.service
%endif

%post notification
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-notification
fi
%else
%systemd_post %{name}-notification.service
%endif

%post api
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-api
fi
%else
%systemd_post %{name}-api.service
%endif

%post central
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-central
fi
%else
%systemd_post %{name}-central.service
%endif

%post alarm
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/chkconfig --add %{name}-${svc}
    done
fi
%else
%systemd_post %{name}-alarm-notifier.service %{name}-alarm-evaluator.service
%endif

%post ipmi
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add %{name}-ipmi
fi
%else
%systemd_post %{name}-alarm-ipmi.service
%endif


%preun compute
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in compute; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-compute.service
%endif

%preun collector
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in collector; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-collector.service
%endif

%preun notification
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in notification; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-notification.service
%endif

%preun api
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in api; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-api.service
%endif

%preun central
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in central; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-central.service
%endif

%preun alarm
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-alarm-notifier.service %{name}-alarm-evaluator.service
%endif

%preun ipmi
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in ipmi; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-ipmi.service
%endif

%preun polling
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -eq 0 ] ; then
    for svc in ipmi; do
        /sbin/service %{name}-${svc} stop > /dev/null 2>&1
        /sbin/chkconfig --del %{name}-${svc}
    done
fi
%else
%systemd_preun %{name}-polling.service
%endif


%postun compute
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in compute; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-compute.service
%endif

%postun collector
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in collector; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-collector.service
%endif

%postun notification
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in notification; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-notification.service
%endif

%postun api
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in api; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-api.service
%endif

%postun central
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in central; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-central.service
%endif

%postun alarm
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in alarm-notifier alarm-evaluator; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-alarm-notifier.service %{name}-alarm-evaluator.service
%endif

%postun ipmi
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in ipmi; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-ipmi.service
%endif

%postun polling
%if 0%{?rhel} && 0%{?rhel} <= 6
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    for svc in ipmi; do
        /sbin/service %{name}-${svc} condrestart > /dev/null 2>&1 || :
    done
fi
%else
%systemd_postun_with_restart %{name}-polling.service
%endif


%files common
%dir %{_sysconfdir}/ceilometer
#if $older_than('2014.2')
%attr(-, root, ceilometer) %{_datadir}/ceilometer/ceilometer-dist.conf
%configfile %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/ceilometer.conf
%configfile %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/policy.json
%configfile %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/pipeline.yaml
#else
%configfile %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/*
#end if

%configfile %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0755, ceilometer, root) %{_localstatedir}/log/ceilometer
%dir %attr(0755, ceilometer, root) %{_localstatedir}/run/ceilometer

%defattr(-, ceilometer, ceilometer, -)
%dir %{_sharedstatedir}/ceilometer
%dir %{_sharedstatedir}/ceilometer/tmp

%post -n python-ceilometer
mkdir -p /opt/openstack/%{python_name}
tar -zxvf /opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{os_release}-venv.tar.gz -C / > /dev/null
ln -fsn /opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{os_release}-venv/venv /opt/openstack/%{python_name}/venv

%files -n python-ceilometer
#venv tarball
/opt/openstack/%{python_name}/*

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%files compute
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{name}-compute
%else
%{_unitdir}/%{name}-compute.service
%endif

%files collector
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{name}-collector
%else
%{_unitdir}/%{name}-collector.service
%endif

%files api
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{name}-api
%else
%{_unitdir}/%{name}-api.service
%endif

%files central
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{name}-central
%else
%{_unitdir}/%{name}-central.service
%endif

%files alarm
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{name}-alarm-notifier
%{_initrddir}/%{name}-alarm-evaluator
%else
%{_unitdir}/%{name}-alarm-notifier.service
%{_unitdir}/%{name}-alarm-evaluator.service
%endif

%files notification
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{name}-notification
%else
%{_unitdir}/%{name}-notification.service
%endif

%files ipmi
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-ipmi
%else
%{_unitdir}/%{name}-ipmi.service
%endif

%files polling
%if 0%{?rhel} && 0%{?rhel} <= 6
%{_initrddir}/%{name}-polling
%else
%{_unitdir}/%{name}-polling.service
%endif

%changelog
