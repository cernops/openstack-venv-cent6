#encoding UTF-8
# Based on spec by:
# * Terry Wilson <twilson@redhat.com>
# * Alan Pevec <apevec@redhat.com>
# * Martin Magr <mmagr@redhat.com>
# * Gary Kotton <gkotton@redhat.com>
# * Robert Kukura <rkukura@redhat.com>
# * Pádraig Brady <P@draigBrady.com>


%global python_name neutron
%global daemon_prefix openstack-neutron
%global os_version 2015.1.0.3
%global no_tests $no_tests
%global tests_data_dir %{_datarootdir}/%{python_name}-tests

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 6)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           openstack-neutron
Version:        %{os_version}.gdkilo.0
Release:        6
Epoch:          2
Summary:        Virtual network service for OpenStack (neutron)

Group:          Applications/System
License:        ASL 2.0
URL:            http://launchpad.net/neutron/

Source0:        %{python_name}-%{os_version}.tar.gz
Source1:	      neutron.logrotate
Source2:	      neutron-sudoers

%if ! (0%{?rhel} > 6)
Source10:	      neutron-server.init
Source11:	      neutron-linuxbridge-agent.init
Source12:	      neutron-openvswitch-agent.init
Source14:	      neutron-nec-agent.init
Source15:       neutron-dhcp-agent.init
Source16:       neutron-l3-agent.init
Source17:	      neutron-ovs-cleanup.init
Source20:       neutron-metadata-agent.init
Source22:       neutron-mlnx-agent.init
Source24:       neutron-metering-agent.init
Source25:       neutron-sriov-nic-agent.init
Source27:       neutron-netns-cleanup.init
%else
Source10:       neutron-server.service
Source11:       neutron-linuxbridge-agent.service
Source12:       neutron-openvswitch-agent.service
Source14:       neutron-nec-agent.service
Source15:       neutron-dhcp-agent.service
Source16:       neutron-l3-agent.service
Source17:       neutron-ovs-cleanup.service
Source20:       neutron-metadata-agent.service
Source22:       neutron-mlnx-agent.service
Source24:       neutron-metering-agent.service
Source25:       neutron-sriov-nic-agent.service
Source27:       neutron-netns-cleanup.service
%endif

Source50:       neutron-rootwrap
Source51:       neutron-rootwrap.conf
Source52:       neutron-policy.json

BuildArch:	    noarch

Requires:	python-neutron = %{epoch}:%{version}-%{release}

Provides:       openstack-neutron = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum < %{epoch}:%{version}-%{release}

%if ! 0%{?usr_only}
Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(pre):    shadow-utils
%endif

%description
Neutron is a virtual network service for Openstack. Just like OpenStack
Nova provides an API to dynamically request and configure virtual
servers, Neutron provides an API to dynamically request and configure
virtual networks. These networks connect "interfaces" from other
OpenStack services (e.g., virtual NICs from Nova VMs). The Neutron API
supports extensions to provide advanced network capabilities (e.g., QoS,
ACLs, network monitoring, etc.)


%package -n python-neutron
Summary:	Neutron Python libraries
Group:		Applications/System

Provides:       python-neutron = %{epoch}:%{version}-%{release}
Obsoletes:      python-quantum < %{epoch}:%{version}-%{release}

Requires:	sudo
Requires:       rsync
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 6)
Requires:       python27
%endif

%description -n python-neutron
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron Python library.

%package -n openstack-neutron-common
Summary:        Neutron common files
Group:          Applications/System

Requires:       python-neutron = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-common
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains Neutron common files.

%package -n openstack-neutron-bigswitch
Summary:	Neutron Big Switch plugin
Group:		Applications/System

Provides:       openstack-neutron-bigswitch = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-bigswitch < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-bigswitch
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using the FloodLight Openflow Controller or the Big Switch
Networks Controller.


%package -n openstack-neutron-brocade
Summary:	Neutron Brocade plugin
Group:		Applications/System

Provides:       openstack-neutron-brocade = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-brocade < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-brocade
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using Brocade VCS switches running NOS.

%package -n openstack-neutron-cisco
Summary:	Neutron Cisco plugin
Group:		Applications/System

Provides:       openstack-neutron-cisco = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-cisco < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-cisco
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using Cisco UCS and Nexus.


%package -n openstack-neutron-embrane
Summary:	Neutron Embrane plugin
Group:		Applications/System

Provides:       openstack-neutron-embrane = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-embrane < %{epoch}:%{version}-%{release}


Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-embrane
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using Embrane heleos platform.
#end if


#if $newer_than_eq('2014.1.b1')
%package -n openstack-neutron-ibm
Summary:        Neutron IBM plugin
Group:          Applications/System

Provides:       openstack-neutron-ibm = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-ibm < %{epoch}:%{version}-%{release}

Requires:       openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-ibm
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using IBM.
#end if

%package -n openstack-neutron-linuxbridge
Summary:	Neutron linuxbridge plugin
Group:		Applications/System

Provides:       openstack-neutron-linuxbridge = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-linuxbridge < %{epoch}:%{version}-%{release}

Requires:	bridge-utils
Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-linuxbridge
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks as VLANs using Linux bridging.


%package -n openstack-neutron-metering-agent
Summary:        Neutron bandwidth metering agent
Group:          Applications/System

Requires:       openstack-neutron-common = %{epoch}:%{version}-%{release}

%description -n openstack-neutron-metering-agent
Neutron provides an API to measure bandwidth utilization

This package contains the Neutron agent responsible for generating bandwidth
utilization notifications.


%package -n openstack-neutron-midonet
Summary:	Neutron MidoNet plugin
Group:		Applications/System

Provides:       openstack-neutron-midonet = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-midonet < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-midonet
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using MidoNet from Midokura.


%package -n openstack-neutron-ml2
Summary:	Neutron ML2 plugin
Group:		Applications/System

Provides:       openstack-neutron-ml2 = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-ml2 < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-ml2
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains a neutron plugin that allows the use of drivers to
support separately extensible sets of network types and the mechanisms
for accessing those types.


%package -n openstack-neutron-mellanox
#end if
Summary:	Neutron Mellanox plugin
Group:		Applications/System

Provides:       openstack-neutron-mlnx = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-mlnx < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}

%description -n openstack-neutron-mellanox

Neutron provides an API to dynamically request and configure virtual
networks.

This plugin implements Quantum v2 APIs with support for Mellanox
embedded switch functionality as part of the VPI (Ethernet/InfiniBand)
HCA.


%package -n openstack-neutron-nuage
Summary:	Neutron Nuage plugin
Group:		Applications/System

Provides:       openstack-neutron-nuage = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-nuage < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-nuage
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using Nuage Networks’ Virtual Service Platform (VSP).


%package -n openstack-neutron-ofagent
Summary:        Neutron ofagent plugin
Group:          Applications/System

Provides:       openstack-neutron-ofagent = %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-ofagent
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using ofagent.
#end if


%package -n openstack-neutron-opencontrail
Summary:        Neutron OpenContrail plugin
Group:          Applications/system

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-opencontrail
This plugin implements Neutron v2 APIs with support for the OpenContrail
plugin.


%package -n openstack-neutron-openvswitch
Summary:	Neutron openvswitch plugin
Group:		Applications/System

Provides:       openstack-neutron-openvswitch = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-openvswitch < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}
Requires:	openvswitch


%description -n openstack-neutron-openvswitch
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using Open vSwitch.


%package -n openstack-neutron-oneconvergence-nvsd
Summary:        Neutron oneconvergence plugin
Group:          Applications/System

Provides:       openstack-neutron-oneconvergence-nvsd = %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}



%description -n openstack-neutron-oneconvergence-nvsd
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using oneconvergence nvsd.


%package -n openstack-neutron-ovsvapp
Summary:	Neutron OVSvApp vSphere plugin
Group:		Applications/System

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}

%description ovsvapp
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using OVSvApp vSphere L2 agent.


%package -n openstack-neutron-plumgrid
Summary:	Neutron PLUMgrid plugin
Group:		Applications/System

Provides:       openstack-neutron-plumgrid = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-plumgrid < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}

%description -n openstack-neutron-plumgrid
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using the PLUMgrid platform.


%package -n openstack-neutron-ryu
Summary:	Neutron Ryu plugin
Group:		Applications/System

Provides:       openstack-neutron-ryu = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-ryu < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}

%description -n openstack-neutron-ryu
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using the Ryu Network Operating System.


%package -n openstack-neutron-sriov-nic-agent
Summary:        Neutron SR-IOV NIC agent
Group:          Applications/system

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}

%description -n openstack-neutron-sriov-nic-agent
Neutron allows to run virtual instances using SR-IOV NIC hardware

This package contains the Neutron agent to support advanced features of
SR-IOV network cards.


%package -n openstack-neutron-nec
Summary:	Neutron NEC plugin
Group:		Applications/System

Provides:       openstack-neutron-nec = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-nec < %{epoch}:%{version}-%{release}


Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-nec
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using the NEC OpenFlow controller.


%package -n openstack-neutron-metaplugin
Summary:	Neutron meta plugin
Group:		Applications/System

Provides:       openstack-neutron-metaplugin = %{epoch}:%{version}-%{release}
Obsoletes:      openstack-quantum-metaplugin < %{epoch}:%{version}-%{release}

Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}


%description -n openstack-neutron-metaplugin
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the neutron plugin that implements virtual
networks using multiple other neutron plugins.


%package -n openstack-neutron-vmware
Summary:       Neutron VMWare NSX support
Group:         Applications/System


Requires:	openstack-neutron-common = %{epoch}:%{version}-%{release}

Provides:      openstack-neutron-vmware = %{epoch}:%{version}-%{release}
Obsoletes:     openstack-neutron-nicera < %{epoch}:%{version}-%{release}

%description -n openstack-neutron-vmware
Neutron provides an API to dynamically request and configure virtual
networks.

This package adds VMWare NSX support for Neutron,



%prep
%setup -q -n neutron-%{os_version}


%install
rm -rf %{buildroot}

#venv tarball
install -p -D -m 644 %{python_name}-%{os_version}-%{release}-venv.tar.gz %{buildroot}/opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{release}-venv.tar.gz

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-neutron

# Install sudoers
install -p -D -m 440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/neutron

#end raw
# Install sysv init scripts
%if ! (0%{?rhel} > 6)
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{daemon_prefix}-server
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{daemon_prefix}-linuxbridge-agent
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{daemon_prefix}-openvswitch-agent
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/%{daemon_prefix}-nec-agent
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/%{daemon_prefix}-dhcp-agent
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{daemon_prefix}-l3-agent
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{daemon_prefix}-ovs-cleanup
install -p -D -m 755 %{SOURCE20} %{buildroot}%{_initrddir}/%{daemon_prefix}-metadata-agent
install -p -D -m 755 %{SOURCE22} %{buildroot}%{_initrddir}/%{daemon_prefix}-mlnx-agent
install -p -D -m 755 %{SOURCE24} %{buildroot}%{_initrddir}/%{daemon_prefix}-metering-agent
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_initrddir}/%{daemon_prefix}-sriov-nic-agent
install -p -D -m 755 %{SOURCE27} %{buildroot}%{_initrddir}/%{daemon_prefix}-netns-cleanup
%else
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_unitdir}/%{daemon_prefix}-server.service
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_unitdir}/%{daemon_prefix}-linuxbridge-agent.service
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_unitdir}/%{daemon_prefix}-openvswitch-agent.service
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_unitdir}/%{daemon_prefix}-nec-agent.service
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_unitdir}/%{daemon_prefix}-dhcp-agent.service
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_unitdir}/%{daemon_prefix}-l3-agent.service
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_unitdir}/%{daemon_prefix}-ovs-cleanup.service
install -p -D -m 755 %{SOURCE20} %{buildroot}%{_unitdir}/%{daemon_prefix}-metadata-agent.service
install -p -D -m 755 %{SOURCE22} %{buildroot}%{_unitdir}/%{daemon_prefix}-mlnx-agent.service
install -p -D -m 755 %{SOURCE24} %{buildroot}%{_unitdir}/%{daemon_prefix}-metering-agent.service
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_unitdir}/%{daemon_prefix}-sriov-nic-agent.service
install -p -D -m 755 %{SOURCE27} %{buildroot}%{_unitdir}/%{daemon_prefix}-netns-cleanup.service
%endif

# Setup directories
mkdir -p %{buildroot}%{_sysconfdir}/neutron/plugins
mkdir -p %{buildroot}%{_datarootdir}/neutron/rootwrap
install -d -m 755 %{buildroot}%{_sharedstatedir}/neutron
install -d -m 755 %{buildroot}%{_localstatedir}/log/neutron
install -d -m 755 %{buildroot}%{_localstatedir}/lock/neutron
install -d -m 755 %{buildroot}%{_localstatedir}/run/neutron

# Create configuration directories for all services that can be populated by users with custom *.conf files
mkdir -p %{buildroot}/%{_sysconfdir}/neutron/conf.d/common

# Create and populate configuration directory for L3 agent that is not accessible for user modification
mkdir -p %{buildroot}%{_datadir}/neutron/l3_agent

# Create dist configuration directory for neutron-server (may be filled by advanced services)
mkdir -p %{buildroot}%{_datadir}/neutron/server

# Create configuration directories for all services that can be populated by users with custom *.conf files
mkdir -p %{buildroot}/%{_sysconfdir}/neutron/conf.d/common
for service in server ovs-cleanup netns-cleanup; do
    mkdir -p %{buildroot}/%{_sysconfdir}/neutron/conf.d/neutron-$service
done
for service in linuxbridge openvswitch nec dhcp l3 metadata mlnx metering sriov-nic; do
    mkdir -p %{buildroot}/%{_sysconfdir}/neutron/conf.d/neutron-$service-agent
done

# Install version info file
cat > %{buildroot}%{_sysconfdir}/neutron/release <<EOF
[Neutron]
vendor = OpenStack LLC
product = OpenStack Neutron
package = %{release}
EOF

# Install rootwrap fix ups
install -p -D -m 555 %{SOURCE50} %{buildroot}%{_bindir}/neutron-rootwrap
install -p -D -m 755 %{SOURCE51} %{buildroot}%{_sysconfdir}/neutron/rootwrap.conf
install -p -D -m 640 -o root -g neutron %{SOURCE52} %{buildroot}%{_sysconfdir}/neutron/policy.json

%clean
rm -rf %{buildroot}


%if ! 0%{?usr_only}
%pre
getent group neutron >/dev/null || groupadd -r neutron
getent passwd neutron >/dev/null || \
useradd -r -g neutron -d %{_sharedstatedir}/neutron -s /sbin/nologin \
-c "OpenStack Neutron Daemons" neutron
exit 0

# Do not autostart daemons in %post since they are not configured yet
#end raw
#if $older_than('2014.2')
#set $daemon_map = {"": ["server", "dhcp-agent", "l3-agent"], "linuxbridge": ["linuxbridge-agent"], "openvswitch": ["openvswitch-agent", "ovs-cleanup"], "ryu": ["ryu-agent"], "nec": ["nec-agent"]}
#end if
#if $newer_than_eq('2014.2')
#set $daemon_map = {"": ["server", "dhcp-agent", "l3-agent", "lbaas-agent", "netns-cleanup"], "linuxbridge": ["linuxbridge-agent"], "openvswitch": ["openvswitch-agent", "ovs-cleanup"], "ryu": ["ryu-agent"], "nec": ["nec-agent"], "mlnx": ["mlnx-agent"], "vpn-agent": ["vpn-agent"], "metering-agent": ["metering-agent"], "sriov-nic-agent": ["sriov-nic-agent"], "cisco": ["cisco-cfg-agent"]}
#end if
#if $newer_than_eq('2015.1')
#set $daemon_map = {"": ["server", "dhcp-agent", "l3-agent", "netns-cleanup"], "linuxbridge": ["linuxbridge-agent"], "openvswitch": ["openvswitch-agent", "ovs-cleanup"], "nec": ["nec-agent"], "metering-agent": ["metering-agent"], "sriov-nic-agent": ["sriov-nic-agent"]}
#end if
#for $key, $value in $daemon_map.iteritems()
#set $daemon_list = " ".join($value) if $value else $key

#%if 0%{?rhel} > 6
#%post $key
#if [ \$1 -eq 1 ] ; then
#    # Initial installation
#    for svc in $daemon_list; do
#        /usr/bin/systemctl preset %{daemon_prefix}-\${svc}.service
#    done
#fi
%endif

#%preun $key
#if [ \$1 -eq 0 ] ; then
#    for svc in $daemon_list; do
#%if ! (0%{?rhel} > 6)
#        /sbin/service %{daemon_prefix}-\${svc} stop &>/dev/null
#        /sbin/chkconfig --del %{daemon_prefix}-\${svc}
#%else
#        /usr/bin/systemctl --no-reload disable %{daemon_prefix}-\${svc}.service > /dev/null 2>&1 || :
#        /usr/bin/systemctl stop %{daemon_prefix}-\${svc}.service > /dev/null 2>&1 || :
#%endif
#    done
#    exit 0
#fi

#end for
#%endif

%post -n python-neutron
mkdir -p /opt/openstack/%{python_name}
tar -zxvf /opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{release}-venv.tar.gz -C /
ln -fsn /opt/openstack/%{python_name}/%{python_name}-%{os_version}-%{release}-venv/venv /opt/openstack/%{python_name}/venv


%files

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-server
%{_initrddir}/%{daemon_prefix}-dhcp-agent
%{_initrddir}/%{daemon_prefix}-l3-agent
%{_initrddir}/%{daemon_prefix}-metadata-agent
%{_initrddir}/%{daemon_prefix}-netns-cleanup
%else
%{_unitdir}/%{daemon_prefix}-server.service
%{_unitdir}/%{daemon_prefix}-dhcp-agent.service
%{_unitdir}/%{daemon_prefix}-l3-agent.service
%{_unitdir}/%{daemon_prefix}-metadata-agent.service
%{_unitdir}/%{daemon_prefix}-netns-cleanup.service
%endif

%dir %{_sysconfdir}/neutron
%{_sysconfdir}/neutron/release
%dir %{_datadir}/neutron/l3_agent
%dir %{_datadir}/neutron/server

%attr(0640, root, neutron) %{_sysconfdir}/neutron/policy.json
%endif

%post
mkdir -p /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/dhcp.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/l3.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/debug.filters /etc/neutron/rootwrap.d/
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/dhcp-agent.ini /etc/neutron/
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/l3-agent.ini /etc/neutron/
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/metadata_agent.ini /etc/neutron/
rsync -a /opt/openstack/neutron/venv/etc/neutron/policy.json /etc/neutron/
chown root:neutron /etc/neutron/policy.json
chmod 0640 /etc/neutron/policy.json


%files -n python-neutron
#venv tarball
/opt/openstack/%{python_name}/*


%files -n openstack-neutron-common

%{_bindir}/neutron-rootwrap

%{_sysconfdir}/neutron/rootwrap.conf
%dir %{_sysconfdir}/neutron
%dir %{_sysconfdir}/neutron/conf.d
%dir %{_sysconfdir}/neutron/conf.d/common
%dir %{_sysconfdir}/neutron/plugins
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sudoers.d/neutron
%dir %attr(0755, neutron, neutron) %{_sharedstatedir}/neutron
%dir %attr(0750, neutron, neutron) %{_localstatedir}/log/neutron
%dir %attr(0755, neutron, neutron) %{_localstatedir}/lock/neutron
%dir %attr(0755, neutron, neutron) %{_localstatedir}/run/neutron
%dir %{_datarootdir}/neutron
%dir %{_datarootdir}/neutron/rootwrap

%post -n openstack-neutron-common
mkdir -p /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/dhcp.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/l3.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/debug.filters /etc/neutron/rootwrap.d/
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/api-paste.ini /etc/neutron/
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/neutron.conf /etc/neutron/
rsync -a /opt/openstack/neutron/venv/etc/neutron/rootwrap.conf /etc/neutron/


%files -n openstack-neutron-bigswitch

%post -n openstack-neutron-bigswitch
mkdir -p /etc/neutron/plugins/bigswitch
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/bigswitch /etc/neutron/plugins/bigswitch


%files -n openstack-neutron-brocade

%post -n openstack-neutron-brocade
mkdir -p /etc/neutron/plugins/brocade
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/brocade /etc/neutron/plugins/brocade


%files -n openstack-neutron-cisco

%post -n openstack-neutron-cisco
mkdir -p /etc/neutron/plugins/cisco
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/cisco /etc/neutron/plugins/cisco


%files -n openstack-neutron-ibm

%post -n openstack-neutron-ibm
mkdir -p /etc/neutron/plugins/ibm
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/ibm /etc/neutron/plugins/ibm

%files -n openstack-neutron-linuxbridge

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-linuxbridge-agent
%else
%{_unitdir}/%{daemon_prefix}-linuxbridge-agent.service
%endif
%endif

%post -n openstack-neutron-linuxbridge
mkdir -p /etc/neutron/plugins/linuxbridge
mkdir -p /etc/neutron/rootwrap.d/
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/linuxbridge /etc/neutron/plugins/linuxbridge
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/linuxbridge-plugin.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/iptables-firewall.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/ipset-firewall.filters /etc/neutron/rootwrap.d/


%files -n openstack-neutron-metering-agent

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-metering-agent
%else
%{_unitdir}/%{daemon_prefix}-metering-agent.service
%endif
%endif

%post -n openstack-neutron-metering-agent
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/metering_agent.ini /etc/neutron/

%files -n openstack-neutron-midonet

%post -n openstack-neutron-midonet
mkdir -p /etc/neutron/plugins/midonet
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/midonet /etc/neutron/plugins/midonet


%files -n openstack-neutron-ml2
%post -n openstack-neutron-ml2
mkdir -p /etc/neutron/plugins/ml2
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/ml2 /etc/neutron/plugins/ml2

%files -n openstack-neutron-mellanox

%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-mlnx-agent
%else
%{_unitdir}/%{daemon_prefix}-mlnx-agent.service
%endif


%post -n openstack-neutron-mellanox
mkdir -p /etc/neutron/plugins/mlnx
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/mlnx /etc/neutron/plugins/mlnx

%files -n openstack-neutron-nuage

%post -n openstack-neutron-nuage
mkdir -p /etc/neutron/plugins/nuage
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/nuage /etc/neutron/plugins/nuage


%files -n openstack-neutron-ofagent


%files -n openstack-neutron-opencontrail

%post -n openstack-neutron-opencontrail
mkdir -p /etc/neutron/plugins/opencontrail
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/opencontrail /etc/neutron/plugins/opencontrail


%files -n openstack-neutron-oneconvergence-nvsd

%post -n openstack-neutron-oneconvergence-nvsd
mkdir -p /etc/neutron/plugins/oneconvergence
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/oneconvergence /etc/neutron/plugins/oneconvergence


%files -n openstack-neutron-openvswitch

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-openvswitch-agent
%{_initrddir}/%{daemon_prefix}-ovs-cleanup
%else
%{_unitdir}/%{daemon_prefix}-openvswitch-agent.service
%{_unitdir}/%{daemon_prefix}-ovs-cleanup.service
%endif
%endif

%post -n openstack-neutron-openvswitch
mkdir -p /etc/neutron/plugins/openvswitch
mkdir -p /etc/neutron/rootwrap.d/
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/openvswitch /etc/neutron/plugins/openvswitch
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/openvswitch-plugin.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/iptables-firewall.filters /etc/neutron/rootwrap.d/
/bin/cp -f /opt/openstack/neutron/venv/etc/neutron/rootwrap.d/ipset-firewall.filters /etc/neutron/rootwrap.d/


%files -n openstack-neutron-ovsvapp

%post -n openstack-neutron-ovsvapp
mkdir -p /etc/neutron/plugins/ovsvapp
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/ovsvapp /etc/neutron/plugins/ovsvapp


%files -n openstack-neutron-plumgrid

%post -n openstack-neutron-plumgrid
mkdir -p /etc/neutron/plugins/plumgrid
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/plumgrid /etc/neutron/plugins/plumgrid


%files -n openstack-neutron-sriov-nic-agent

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-sriov-nic-agent
%else
%{_unitdir}/%{daemon_prefix}-sriov-nic-agent.service
%endif
%endif


%files -n openstack-neutron-nec

%if ! 0%{?usr_only}
%if ! (0%{?rhel} > 6)
%{_initrddir}/%{daemon_prefix}-nec-agent
%else
%{_unitdir}/%{daemon_prefix}-nec-agent.service
%endif
%endif

%post -n openstack-neutron-nec
mkdir -p /etc/neutron/plugins/nec
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/nec /etc/neutron/plugins/nec


%files -n openstack-neutron-vmware

%post -n openstack-neutron-vmware
mkdir -p /etc/neutron/plugins/vmware
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/vmware /etc/neutron/plugins/vmware

%files -n openstack-neutron-metaplugin

%post -n openstack-neutron-metaplugin
mkdir -p /etc/neutron/plugins/metaplugin
rsync -a --ignore-existing /opt/openstack/neutron/venv/etc/neutron/plugins/metaplugin /etc/neutron/plugins/metaplugin

%changelog
