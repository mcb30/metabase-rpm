#
# WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
#
# This is a placeholder RPM.  It does *not* build Metabase from
# source: instead it downloads the published binary (metabase.jar).
#
# The purpose of this RPM is to allow for downstream infrastructure
# (such as Puppet manifests) to consume Metabase as though it were
# properly packaged.
#
# WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
#

Name:		metabase
Version:	0.35.4
Release:	2%{?dist}
Summary:	Metabase data visualisation tool
License:	Affero GPLv3
URL:		https://www.metabase.com
Source0:	https://downloads.metabase.com/v%{version}/%{name}.jar
Source1:	%{name}-sysusers.conf
Source2:	%{name}.service
Source3:	%{name}-defaults.conf
Source4:	%{name}-httpd.conf
BuildArch:	noarch
BuildRequires:	systemd-rpm-macros
Requires:	jre-headless
Requires:	httpd-filesystem

%description
Metabase is an open source business intelligence tool.  It lets you ask
questions about your data and visualise the answers.

%prep
%autosetup -c -T

%build

%install
mkdir -p %{buildroot}/%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}/%{_datadir}/%{name}
mkdir -p %{buildroot}/%{_prefix}/lib/%{name}/plugins
install -D -m 644 %{SOURCE0} %{buildroot}%{_libexecdir}/%{name}.jar
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/10-defaults.conf
install -D -m 644 %{SOURCE4} \
	%{buildroot}%{_sysconfdir}/httpd/conf.d/50-%{name}.conf

%pre
%sysusers_create_package %{name} %{SOURCE1}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%dir %attr(0770, %{name}, %{name}) %{_sharedstatedir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_prefix}/lib/%{name}/plugins
%config(noreplace) %{_sysconfdir}/%{name}/10-defaults.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/50-%{name}.conf
%{_libexecdir}/%{name}.jar
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service

%changelog
* Tue Jun 23 2020 Michael Brown <mbrown@fensystems.co.uk> - 0.35.4-2
- Add httpd.conf fragment

* Mon Jun 22 2020 Michael Brown <mbrown@fensystems.co.uk> - 0.35.4-1
- First placeholder package
