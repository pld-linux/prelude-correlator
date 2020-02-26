# TODO: verify if %%py_postclean can be done
Summary:	Real time correlator of events received by Prelude Manager
Summary(pl.UTF-8):	Narzędzie kojarzące w czasie rzeczywistym zdarzenia odebrane przez Prelude Managera
Name:		prelude-correlator
Version:	5.1.0
Release:	1
License:	GPL v2+
Group:		Applications/Networking
#Source0Download: https://www.prelude-siem.org/projects/prelude/files
Source0:	https://www.prelude-siem.org/attachments/download/1173/%{name}-%{version}.tar.gz
# Source0-md5:	0916b2391a35ed7a4808ba7c8656d833
Source1:	%{name}.init
Patch0:		%{name}-vardir.patch
URL:		https://www.prelude-siem.org/
BuildRequires:	python-devel
BuildRequires:	python-setuptools >= 0.6-2.c11
BuildRequires:	rpmbuild(macros) >= 1.714
Requires(pre):	/usr/sbin/useradd
Requires(post):	/sbin/chkconfig
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires(postun):	/sbin/service
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prelude-Correlator allows conducting multi-stream correlations thanks
to a powerful programming language for writing correlation rules. With
any type of alert able to be correlated, event analysis becomes
simpler, quicker and more incisive. This correlation alert then
appears within the Prewikka interface and indicates the potential
target information via the set of correlation rules.

%description -l pl.UTF-8
Prelude-Correlator pozwala na wykonywanie wielostrumieniowych
skojarzeń dzięki potężnemu językowi programowania do tworzenia reguł
korelacji. Dzięki możliwości skorelowania dowolnego rodzaju alarmu,
analiza zdarzeń robi się prostsza, szybsza i dokładniejsza. Tak
skorelowane alarmy pojawiają się następnie w interfejsie Prewikki i
określają potencjalną informację o celu poprzez zbiór reguł korelacji.

%prep
%setup -q
%patch0 -p1

%build
%py_build

%install
rm -rf $RPM_BUILD_ROOT

%py_install

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
        %service -q %{name} stop
        /sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(700,root,root) %dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{_sysconfdir}/%{name}/rules
%dir %{_sysconfdir}/%{name}/rules/python
%{_sysconfdir}/%{name}/rules/python/*.py
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_var}/lib/%{name}
%{_var}/lib/%{name}/*.dat
%{py_sitescriptdir}/preludecorrelator
%{py_sitescriptdir}/prelude_correlator-%{version}-py*.egg-info
