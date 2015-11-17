%define _binaries_in_noarch_packages_terminate_build   0

%global python_name nova
%global daemon_prefix openstack-nova
%global os_version 2015.1.1.dev450
%global os_release 1
%global no_tests $no_tests
%global tests_data_dir %{_datarootdir}/%{python_name}-tests

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 6)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif


Name:             openstack-nova
Summary:          OpenStack Compute (nova)
Version:          %{os_version}
Release:          %{os_release}%{?dist}

Group:            Development/Languages
License:          ASL 2.0
Vendor:           OpenStack Foundation
URL:              http://openstack.org/projects/compute/
Source0:          %{python_name}-%{os_version}.tar.gz

%if ! (0%{?rhel} > 6)
Source10:         openstack-nova-api.init
Source11:         openstack-nova-cert.init
Source12:         openstack-nova-compute.init
Source13:         openstack-nova-network.init
Source14:         openstack-nova-objectstore.init
Source15:         openstack-nova-scheduler.init
Source18:         openstack-nova-xvpvncproxy.init
Source19:         openstack-nova-console.init
Source20:         openstack-nova-consoleauth.init
Source25:         openstack-nova-metadata-api.init
Source26:         openstack-nova-conductor.init
Source27:         openstack-nova-cells.init
Source28:         openstack-nova-spicehtml5proxy.init
Source29:         openstack-nova-serialproxy.init
%else
Source10:         openstack-nova-api.service
Source11:         openstack-nova-cert.service
Source12:         openstack-nova-compute.service
Source13:         openstack-nova-network.service
Source14:         openstack-nova-objectstore.service
Source15:         openstack-nova-scheduler.service
Source18:         openstack-nova-xvpvncproxy.service
Source19:         openstack-nova-console.service
Source20:         openstack-nova-consoleauth.service
Source25:         openstack-nova-metadata-api.service
Source26:         openstack-nova-conductor.service
Source27:         openstack-nova-cells.service
Source28:         openstack-nova-spicehtml5proxy.service
Source29:         openstack-nova-serialproxy.service
%endif

Source50:         nova-ifc-template
Source51:         nova.logrotate
Source52:         nova-polkit.pkla
Source53:         nova-sudoers
Source54:         nova-rootwrap
Source55:         policy.json
Source56:         api-paste.ini
Source57:         nova.conf
Source58:         rootwrap.conf

Source60:         api-metadata.filters
Source61:         baremetal-compute-ipmi.filters
Source62:         baremetal-deploy-helper.filters
Source63:         compute.filters
Source64:         network.filters

Source70:         guestfs.py
Source71:         libguestfsmod.so


BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}

BuildArch:        noarch

Requires:         %{name}-compute = %{version}-%{release}
Requires:         %{name}-cert = %{version}-%{release}
Requires:         %{name}-scheduler = %{version}-%{release}
Requires:         %{name}-api = %{version}-%{release}
Requires:         %{name}-network = %{version}-%{release}
Requires:         %{name}-objectstore = %{version}-%{release}
Requires:         %{name}-console = %{version}-%{release}

%description
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

%package common
Summary:          Components common to all OpenStack services
Group:            Applications/System

Requires:         python-nova = %{version}-%{release}

%if ! 0%{?usr_only}
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(pre):    shadow-utils
%endif


%description common
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains scripts, config and dependencies shared
between all the OpenStack nova services.

%package compute
Summary:          OpenStack Nova Virtual Machine control service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}
Requires:         curl
Requires:         iscsi-initiator-utils
Requires:         iptables iptables-ipv6
Requires:         vconfig
# tunctl is needed where `ip tuntap` is not available
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 6)
Requires:         tunctl
Requires:         libguestfs-mount >= 1.7.17
%else
#latest libguestfs-tools for cent7 doesn't provide requires for
#libguestfs-mount
Requires:         libguestfs-tools   >= 1.7.17
Requires:         libguestfs-tools-c >= 1.7.17
%endif
# The fuse dependency should be added to libguestfs-mount
Requires:         fuse
Requires:         libvirt >= 0.8.7
Requires(pre):    qemu-kvm
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 6)
Requires:         python27
%endif

%description compute
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service for controlling Virtual Machines.


%package network
Summary:          OpenStack Nova Network control service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}
Requires:         vconfig
Requires:         radvd
Requires:         bridge-utils
Requires:         dnsmasq-utils
Requires:         dnsmasq
# tunctl is needed where `ip tuntap` is not available
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 6)
Requires:         tunctl
%endif

%description network
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service for controlling networking.


%package scheduler
Summary:          OpenStack Nova VM distribution service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description scheduler
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the service for scheduling where
to run Virtual Machines in the cloud.


%package cert
Summary:          OpenStack Nova certificate management service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description cert
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service for managing certificates.


%package api
Summary:          OpenStack Nova API services
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description api
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova services providing programmatic access.


%package conductor
Summary:          OpenStack Nova Conductor services
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description conductor
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova services providing database access for
the compute service


%package objectstore
Summary:          OpenStack Nova simple object store service
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description objectstore
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova service providing a simple object store.


%package console
Summary:          OpenStack Nova console access services
Group:            Applications/System

Requires:         %{name}-common = %{version}-%{release}

%description console
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova services providing console access
services to Virtual Machines.


%package cells
Summary:          OpenStack Nova Cells services
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description cells
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova Cells service providing additional
scaling and (geographic) distribution for compute services.

#if $newer_than_eq('2014.2')
%package serialproxy
Summary:          OpenStack Nova serial console access service
Group:            Applications/System

Requires:         openstack-nova-common = %{version}-%{release}

%description serialproxy
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform. It gives you the
software, control panels, and APIs required to orchestrate a cloud,
including running instances, managing networks, and controlling access
through users and projects. OpenStack Compute strives to be both
hardware and hypervisor agnostic, currently supporting a variety of
standard hardware configurations and seven major hypervisors.

This package contains the Nova services providing the
serial console access service to Virtual Machines.
#end if

%package -n       python-nova
Summary:          Nova Python libraries
Group:            Applications/System

Requires:         openssl
Requires:         sudo

%description -n   python-nova
OpenStack Compute (codename Nova) is open source software designed to
provision and manage large networks of virtual machines, creating a
redundant and scalable cloud computing platform.

This package contains the %{name} Python library.

%prep
%setup0 -q -n %{python_name}-%{os_version}

%install
rm -rf %{buildroot}

install -p -D -m 644 %{python_name}-%{os_version}-%{os_release}-venv.tar.gz %{buildroot}/opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{os_release}-venv.tar.gz
#make sure the /usr/share/nova dirs exist
mkdir -p %{buildroot}/usr/share/nova/rootwrap
mkdir -p %{buildroot}/usr/share/nova/interfaces

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

%if ! 0%{?usr_only}
# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/buckets
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/images
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/instances
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/keys
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/networks
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/nova
install -d -m 755 %{buildroot}%{_localstatedir}/lock/nova

# Setup ghost CA cert
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA
install -d -m 755 %{buildroot}%{_sharedstatedir}/nova/CA/{certs,crl,newcerts,projects,reqs}
touch %{buildroot}%{_sharedstatedir}/nova/CA/{cacert.pem,crl.pem,index.txt,openssl.cnf,serial}
install -d -m 750 %{buildroot}%{_sharedstatedir}/nova/CA/private
touch %{buildroot}%{_sharedstatedir}/nova/CA/private/cakey.pem

# Clean CA directory
find %{buildroot}%{_sharedstatedir}/nova/CA -name .gitignore -delete
find %{buildroot}%{_sharedstatedir}/nova/CA -name .placeholder -delete

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/nova
# Install initscripts for Nova services
%if ! (0%{?rhel} > 6)
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{daemon_prefix}-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{daemon_prefix}-cert
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{daemon_prefix}-compute
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{daemon_prefix}-network
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{daemon_prefix}-objectstore
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{daemon_prefix}-scheduler
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/%{daemon_prefix}-xvpvncproxy
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_initrddir}/%{daemon_prefix}-console
install -p -D -m 755 %{SOURCE20} %{buildroot}%{_initrddir}/%{daemon_prefix}-consoleauth
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_initrddir}/%{daemon_prefix}-metadata-api
install -p -D -m 755 %{SOURCE26} %{buildroot}%{_initrddir}/%{daemon_prefix}-conductor
install -p -D -m 755 %{SOURCE27} %{buildroot}%{_initrddir}/%{daemon_prefix}-cells
install -p -D -m 755 %{SOURCE28} %{buildroot}%{_initrddir}/%{daemon_prefix}-spicehtml5proxy
#if $newer_than_eq('2014.2')
install -p -D -m 755 %{SOURCE29} %{buildroot}%{_initrddir}/%{daemon_prefix}-serialproxy
#end if

#raw
#fix metadata-api bin name
sed -i s?exec=\"/usr/bin/nova-metadata-api\"?exec=\"/usr/bin/nova-api-metadata\"? %{buildroot}%{_initrddir}/%{daemon_prefix}-metadata-api
#end raw
%else
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_unitdir}/%{daemon_prefix}-api.service
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_unitdir}/%{daemon_prefix}-cert.service
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_unitdir}/%{daemon_prefix}-compute.service
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_unitdir}/%{daemon_prefix}-network.service
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_unitdir}/%{daemon_prefix}-objectstore.service
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_unitdir}/%{daemon_prefix}-scheduler.service
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_unitdir}/%{daemon_prefix}-xvpvncproxy.service
install -p -D -m 755 %{SOURCE19} %{buildroot}%{_unitdir}/%{daemon_prefix}-console.service
install -p -D -m 755 %{SOURCE20} %{buildroot}%{_unitdir}/%{daemon_prefix}-consoleauth.service
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_unitdir}/%{daemon_prefix}-metadata-api.service
install -p -D -m 755 %{SOURCE26} %{buildroot}%{_unitdir}/%{daemon_prefix}-conductor.service
install -p -D -m 755 %{SOURCE27} %{buildroot}%{_unitdir}/%{daemon_prefix}-cells.service
install -p -D -m 755 %{SOURCE28} %{buildroot}%{_unitdir}/%{daemon_prefix}-spicehtml5proxy.service
#if $newer_than_eq('2014.2')
install -p -D -m 755 %{SOURCE29} %{buildroot}%{_unitdir}/%{daemon_prefix}-serialproxy.service
#end if
#raw
#fix metadata-api bin name
sed -i s?ExecStart=/usr/bin/nova-metadata-api?ExecStart=/usr/bin/nova-api-metadata? %{buildroot}%{_unitdir}/%{daemon_prefix}-metadata-api.service
#end raw
%endif

# Install sudoers
install -p -D -m 440 %{SOURCE53} %{buildroot}%{_sysconfdir}/sudoers.d/nova

# Install logrotate
install -p -D -m 644 %{SOURCE51} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install policy.json
install -p -D -m 640 %{SOURCE55} %{buildroot}%{_sysconfdir}/nova/policy.json

#Install api-paste.ini
install -p -D -m 640 %{SOURCE56} %{buildroot}%{_sysconfdir}/nova/api-paste.ini

# Install nova.conf
install -p -D -m 644 %{SOURCE57} %{buildroot}%{_sysconfdir}/nova/nova.conf

# Install rootwrap.conf
install -p -D -m 644 %{SOURCE58} %{buildroot}%{_sysconfdir}/nova/rootwrap.conf

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/nova

install -d -m 755 %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d
install -p -D -m 644 %{SOURCE52} %{buildroot}%{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla
%endif

# Install template files

# Install rootwrap files in /usr/share/nova/rootwrap
install -p -D -m 555 %{SOURCE54} %{buildroot}%{_bindir}/nova-rootwrap

# Install rootwrap commands
install -p -D -m 644 %{SOURCE60} %{buildroot}%{_datarootdir}/nova/rootwrap/api-metadata.filters
# install -p -D -m 644 %{SOURCE61} %{buildroot}%{_datarootdir}/nova/rootwrap/baremetal-compute-ipmi.filters
# install -p -D -m 644 %{SOURCE62} %{buildroot}%{_datarootdir}/nova/rootwrap/baremetal-deploy-helper.filters
install -p -D -m 644 %{SOURCE63} %{buildroot}%{_datarootdir}/nova/rootwrap/compute.filters
install -p -D -m 644 %{SOURCE64} %{buildroot}%{_datarootdir}/nova/rootwrap/network.filters

# Network configuration templates for injection engine

# python-libguestfs files
install -p -D -m 644 %{SOURCE70} %{buildroot}/opt/openstack/nova/venv/lib/python2.7/site-packages/guestfs.py
install -p -D -m 644 %{SOURCE71} %{buildroot}/opt/openstack/nova/venv/lib64/python2.7/site-packages/libguestfsmod.so

%clean
rm -rf %{buildroot}

%pre common
getent group nova >/dev/null || groupadd -r nova --gid 162
if ! getent passwd nova >/dev/null; then
  useradd -u 162 -r -g nova -G nova,nobody -d %{_sharedstatedir}/nova -s /sbin/nologin -c "OpenStack Nova Daemons" nova
fi
exit 0

%pre compute
usermod -a -G qemu nova
exit 0

%post
# if %{_sbindir}/selinuxenabled; then
#     echo -e "\033[47m\033[1;31m***************************************************\033[0m"
#     echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
#     echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m >> \033[5mYou have SELinux enabled on your host !\033[25m <<  \033[47m\033[1;31m*\033[0m"
#     echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
#     echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31mPlease disable it by setting \`SELINUX=disabled' \033[47m\033[1;31m*\033[0m"
#     echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31min /etc/sysconfig/selinux and don't forget      \033[47m\033[1;31m*\033[0m"
#     echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31mto reboot your host to apply that change!       \033[47m\033[1;31m*\033[0m"
#     echo -e "\033[47m\033[1;31m*\033[0m \033[40m\033[1;31m                                                \033[47m\033[1;31m*\033[0m"
#     echo -e "\033[47m\033[1;31m***************************************************\033[0m"
# fi

%post -n python-nova
mkdir -p /opt/openstack/%{python_name}
tar -zxvf /opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{os_release}-venv.tar.gz -C /
ln -fsn /opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{os_release}-venv/venv /opt/openstack/%{python_name}/venv
mv -f /opt/openstack/%{python_name}/venv/bin/nova-rootwrap /opt/openstack/%{python_name}/venv/bin/nova-rootwrap-real

%files

%files common

%{_bindir}/nova-rootwrap

%if ! 0%{?usr_only}
%dir %{_sysconfdir}/nova
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-nova
%config(noreplace) %{_sysconfdir}/sudoers.d/nova
%config(noreplace) %{_sysconfdir}/polkit-1/localauthority/50-local.d/50-nova.pkla
%config(noreplace) %attr(0640, root, nova) /etc/nova/policy.json
%config(noreplace) %attr(0640, root, nova) /etc/nova/api-paste.ini
%config(noreplace) %attr(0640, root, nova) /etc/nova/nova.conf
%config(noreplace) %attr(0640, root, nova) /etc/nova/rootwrap.conf
%dir %attr(0755, nova, root) %{_localstatedir}/log/nova
%dir %attr(0755, nova, root) %{_localstatedir}/lock/nova
%dir %attr(0755, nova, root) %{_localstatedir}/run/nova

%defattr(-, nova, nova, -)
%dir %{_sharedstatedir}/nova
%dir %{_sharedstatedir}/nova/buckets
%dir %{_sharedstatedir}/nova/images
%dir %{_sharedstatedir}/nova/instances
%dir %{_sharedstatedir}/nova/keys
%dir %{_sharedstatedir}/nova/networks
%dir %{_sharedstatedir}/nova/tmp
%endif


%files compute
%{_datarootdir}/nova/rootwrap/compute.filters

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-compute
%else
%{_unitdir}/%{daemon_prefix}-compute.service
%endif
%endif

/opt/openstack/nova/venv/lib64/python2.7/site-packages/libguestfsmod.so
/opt/openstack/nova/venv/lib/python2.7/site-packages/guestfs.py
# /opt/openstack/nova/venv/lib/python2.7/site-packages/guestfs.pyc
# /opt/openstack/nova/venv/lib/python2.7/site-packages/guestfs.pyo


%files network
%{_datarootdir}/nova/rootwrap/network.filters

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-network
%else
%{_unitdir}/%{daemon_prefix}-network.service
%endif
%endif


%files scheduler

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-scheduler
%else
%{_unitdir}/%{daemon_prefix}-scheduler.service
%endif
%endif


%files cert
%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-cert
%else
%{_unitdir}/%{daemon_prefix}-cert.service
%endif
%defattr(-, nova, nova, -)
%dir %{_sharedstatedir}/nova/CA/
%dir %{_sharedstatedir}/nova/CA/certs
%dir %{_sharedstatedir}/nova/CA/crl
%dir %{_sharedstatedir}/nova/CA/newcerts
%dir %{_sharedstatedir}/nova/CA/projects
%dir %{_sharedstatedir}/nova/CA/reqs
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/cacert.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/crl.pem
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/index.txt
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/openssl.cnf
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/serial
%dir %attr(0750, -, -) %{_sharedstatedir}/nova/CA/private
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sharedstatedir}/nova/CA/private/cakey.pem
%endif


%files api
%{_datarootdir}/nova/rootwrap/api-metadata.filters

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/openstack-nova-*api
%else
%{_unitdir}/%{daemon_prefix}-*api.service
%endif
%endif


%files conductor

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/openstack-nova-conductor
%else
%{_unitdir}/%{daemon_prefix}-conductor.service
%endif
%endif


%files objectstore
%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-objectstore
%else
%{_unitdir}/%{daemon_prefix}-objectstore.service
%endif
%endif


%files console

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/openstack-nova-console*
%{_initrddir}/openstack-nova-xvpvncproxy
%{_initrddir}/openstack-nova-spicehtml5proxy
%else
%{_unitdir}/%{daemon_prefix}-console*.service
%{_unitdir}/%{daemon_prefix}-xvpvncproxy.service
%{_unitdir}/%{daemon_prefix}-spicehtml5proxy.service
%endif
%endif

#if $newer_than_eq('2014.2')
%files serialproxy

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-serialproxy
%else
%{_unitdir}/%{daemon_prefix}-serialproxy.service
%endif
%endif
#end if

%files cells

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/openstack-nova-cells
%else
%{_unitdir}/%{daemon_prefix}-cells.service
%endif
%endif

%files -n python-nova

#venv tarball
/opt/openstack/%{python_name}/*
%dir /usr/share/nova/interfaces
%dir /usr/share/nova/rootwrap

%if 0%{?with_doc}
%files doc
%doc LICENSE doc/build/html
%endif

%changelog


