Summary:	Real time correlator of events received by Prelude Manager
Name:		prelude-correlator
Version:	1.0.0
Release:	1
License:	GPL v2+
Group:		Applications/Networking
URL:		http://www.prelude-ids.com/
Source0:	http://www.prelude-ids.com/download/releases/prelude-correlator/%{name}-%{version}.tar.gz
# Source0-md5:	d66135ceba28cd6d06dbb29e2963012b
Source1:	%{name}.init
BuildRequires:	python-devel
BuildRequires:	python-setuptools >= 0.6-2.c11
Requires(pre):	/usr/sbin/useradd
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service
Requires:	libprelude-python >= 0.9.24
BuildArch:	noarch
BuildRoot:  %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prelude-Correlator allows conducting multi-stream correlations thanks
to a powerful programming language for writing correlation rules. With
any type of alert able to be correlated, event analysis becomes
simpler, quicker and more incisive. This correlation alert then
appears within the Prewikka interface and indicates the potential
target information via the set of correlation rules.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_initrddir}
install %SOURCE1 $RPM_BUILD_ROOT%{_initrddir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/chkconfig --add %{name}


%preun
if [ $1 = 0 ]; then
        %service %{name} stop > /dev/null 2>&1 || :
        /sbin/chkconfig --del %{name}
fi


%postun
if [ "$1" -ge "1" ]; then
        %service %{name} condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS HACKING.README docs/sample-plugin
%dir %attr(700,root,root) %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%{_initrddir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_var}/lib/%{name}
%{_var}/lib/%{name}/*
%{py_sitescriptdir}/PreludeCorrelator/
%{py_sitescriptdir}/prelude_correlator*.egg-info
