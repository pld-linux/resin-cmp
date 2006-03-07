Summary:	A fast servlet and JSP engine
Summary(pl):	Szybki silnik servletów i JSP
Name:		resin-cmp
Version:	1.0.4
Release:	1
License:	Caucho Developer Source License
Group:		Networking/Daemons/Java
Source0:	http://www.caucho.com/download/%{name}-%{version}.tar.gz
# Source0-md5:	f1f794fd9ed9f8c90c3832a99f2227d5
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}.logrotate
Source10:	%{name}-mod_caucho.conf
Source11:	%{name}-conf_resin.conf
Source12:	%{name}-conf_apache2resin.conf
Source13:	%{name}-conf_examples-params.conf
Source14:	%{name}-conf_examples-webapps.conf
Patch0:		%{name}-configure-test-httpd.conf.patch
Patch1:		%{name}-configure-libssl_so.patch
Patch2:		%{name}-mod_caucho-ipv6.patch
Patch3:		%{name}-makefile_in-jni_include.patch
Patch4:		%{name}-pidfile.patch
URL:		http://www.caucho.com/
BuildRequires:	apache-devel
BuildRequires:	autoconf >= 1.4
BuildRequires:	automake >= 1.4d
BuildRequires:	jdk >= 1.2
BuildRequires:	libtool >= 1.4
BuildRequires:	openssl-devel >= 0.9.7d
Requires(post,preun):	/sbin/chkconfig
Requires:	jdk >= 1.2
Requires:	rc-scripts
Requires:	sed
# it's known it's better to use apache as HTTP server, but
# resin itself has got httpd too.
Provides:	ejb
Provides:	jsp
Provides:	servlet
Provides:	webserver
Conflicts:	resin
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apxs		/usr/sbin/apxs
%define		httpdir		/home/services/httpd
%define		_libexecdir	%{_prefix}/lib/apache

%description
Resin-CMP brings Enterprise Java Bean's container managed persistence
(CMP) to servlet applications, letting modest sites eliminate
hardcoded JDBC calls without requiring the complexity of distributed
objects.

Resin-CMP contains Resin 2.0. Resin is a fast servlet and JSP engine
supporting load balancing for increased reliability. Resin encourages
separation of content from style with its XSL support. Servlets can
generate simple XML and use an XSL filter to format results for each
client's capability, from palm pilots to Mozilla.

%description -l pl
Resin-CMP dostarcza aplikacjom servletowym Enterprise Java Bean's
Container Managed Persistence (CMP), pozwalaj±c przyzwoitym witrynom
wyeliminowaæ wpisane na sta³e wywo³ania JDBC bez potrzeby
komplikowania rozproszonych obiektów.

Resin-CMP zawiera Resina 2.0. Resin to szybki silnik servletowy i JSP,
obs³uguj±cy load balancing aby osi±gn±æ wiêksz± niezawodno¶æ. Resin
wspiera oddzielenie tre¶ci od stylu poprzez obs³ugê XSL. Servlety mog±
generowaæ prosty XML i u¿ywaæ filtra XSL do formatowania wyników
zale¿nie od mo¿liwo¶ci klienta, od Palm Pilotów do Mozilli.

%package doc
Summary:	Additional documentation for Resin
Summary(pl):	Dodatkowa dokumentacja do Resina
Group:		Networking/Daemons/Java
Requires(post):	fileutils
Requires(post):	findutils
Requires:	%{name} = %{version}

%description doc
Documentation for Resin. Contains:
- The Servlet Demos, The FAQ
- Installation configurations: Standalone Resin Web Server Resin with
  Unix Apache, Win32 Apache, IIS, O'Reilly WebSite, Netscape.
- Basic resin.conf: Servlet configuration, Database configuration, Web
  application configuration, HTTP and srun configuration, General Resin
  configuration.
- Servlet Example, Virtual Hosts, Caching, Load Balancing
- The Reference guide, The JavaDoc

%description doc -l pl
Dokumentacja dla Resina. Zawiera:
- servlety demonstracyjne, FAQ
- konfiguracje instalacji: dla samodzielnego Resina, Resina z Apache
  pod Uniksem, z Apache pod Win32, IIS, O'Reilly WebSite, Netscape.
- podstawowy resin.conf: konfiguracja servletów, konfiguracja bazy
  danych, konfiguracja aplikacji WWW, konfiguracja HTTP i srun, ogólna
  konfiguracja Resina
- przyk³ad servletu, wirtualnych hostów, cachowania, load balancingu
- przewodnik, JavaDoc.

%package mod_caucho
Summary:	Resin module for Apache
Summary(pl):	Modu³ Resina dla Apache
Group:		Networking/Daemons
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	%{name} = %{version}
Requires:	apache(EAPI)

%description mod_caucho
Allows to serve JSP requests under Apache.

%description mod_caucho -l pl
Pozwala obs³ugiwaæ ¿±dania JSP spod Apache.

%package hardcore
Summary:	Resin kernel module
Summary(pl):	Modu³ j±dra do Resina
Group:		Networking/Daemons
Requires:	%{name} = %{version}
Provides:	webserver

%description hardcore
Resin HardCore is a Linux kernel module. By pulling the webserver into
the kernel single-computer Resin servers and load-balanced servers can
greatly improve their performance. HardCore replaces Apache as a
web-server, grabbing HTTP requests and passing them to the backend
Resin JVMs. Because HardCore operates entirely in the kernel, it has
very low overhead.

Details at http://localhost:8880/java_tut/hardcore.xtp .

%description hardcore -l pl
Resin HardCore jest modu³em j±dra Linuksa. Poprzez wci±gniêcie serwera
WWW do j±dra, jednokomputerowe serwery Resin, jak i te z
load-balancingiem mog± znacznie poprawiæ wydajno¶æ. HardCore zastêpuje
Apache jako serwer WWW, pobieraj±c zapytania HTTP i przesy³aj±c je do
backendu Resin JVM. Poniewa¿ HardCore dzia³a ca³kowicie w j±drze, ma
bardzo ma³e opó¼nienia.

Szczegó³y na http://localhost:8880/java_tut/hardcore.xtp .

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--with-apache \
	--with-apache-eapi \
	--with-java-home=%{_libdir}/java \
	--with-jni-include=%{_libdir}/java/include \
	--with-openssl=/usr \
	--enable-linux-smp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libexecdir} \
	  $RPM_BUILD_ROOT%{_sysconfdir}/{resin/examples,httpd} \
	  $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,logrotate.d} \
	  $RPM_BUILD_ROOT%{_datadir}/resin/{lib,sql,xsl,libexec} \
	  $RPM_BUILD_ROOT%{httpdir}/resin/webapps \
	  $RPM_BUILD_ROOT%{_localstatedir}/{run,log,log/archiv}/resin \
	  $RPM_BUILD_ROOT%{_localstatedir}/lib/resin/{cache,work,war_expand} \
	  $RPM_BUILD_ROOT%{_bindir}

cp -R bin lib xsl sql $RPM_BUILD_ROOT%{_datadir}/resin
cp -R doc/*  $RPM_BUILD_ROOT%{httpdir}/resin
install src/c/plugin/resin/resin.o $RPM_BUILD_ROOT%{_datadir}/resin/libexec

install %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/mod_caucho.conf

for conf in %{SOURCE11} %{SOURCE12} ; do
	install $conf \
		$RPM_BUILD_ROOT%{_sysconfdir}/resin/$(basename $conf|sed "s/%{name}-conf_//")
done
for conf in %{SOURCE13} %{SOURCE14} ; do
	install $conf \
		$RPM_BUILD_ROOT%{_sysconfdir}/resin/examples/$(basename $conf|sed "s/%{name}-conf_examples-//")
done

install src/c/plugin/apache/mod_caucho.so $RPM_BUILD_ROOT%{_libexecdir}
install src/c/plugin/resin/resin $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/resin
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/resin
install %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d

touch $RPM_BUILD_ROOT/var/log/resin/{access,error,stdout,sterr}_log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add resin
if [ -f %{_localstatedir}/lock/subsys/resin ]; then
	/etc/rc.d/init.d/resin restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/resin start\" to start resin daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_localstatedir}/lock/subsys/resin ]; then
		/etc/rc.d/init.d/resin stop 1>&2
	fi
	/sbin/chkconfig --del resin
fi
rm -rf %{_localstatedir}/lib/resin/cache/*
rm -rf %{httpdir}/resin/WEB-INF/{tmp,work}

%post mod_caucho
%{apxs} -e -a -n caucho %{_libexecdir}/mod_caucho.so 1>&2
if ! grep -q "^Include.*mod_caucho.conf" /etc/httpd/httpd.conf ; then
	echo "Include /etc/httpd/mod_caucho.conf" >> /etc/httpd/httpd.conf
fi
if [ -f %{_localstatedir}/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start httpd daemon."
fi
echo "You may want to uncomment apache2resin.conf in resin.conf"

%preun mod_caucho
if [ "$1" = "0" ]; then
	umask 027
	%{apxs} -e -A -n caucho %{_libexecdir}/mod_caucho.so 1>&2
	grep -v "^Include.*mod_caucho.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f %{_localstatedir}/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
	echo "You may want to disable apache2resin.conf in resin.conf"
fi

%post doc
echo "Setting permissions to WEB-INF directories"
find %{httpdir}/resin -type d -name WEB-INF -exec chown -R root:http {} \; -exec chmod -R g+w {} \;
echo "Don't forget to uncomment examples in resin.conf and restart resin-cmp"

%preun doc
echo "Don't forget to disable examples in resin.conf and restart resin-cmp"

%files
%defattr(644,root,root,755)
%doc LICENSE readme.txt conf/*
%attr(750,root,http) %dir %{_sysconfdir}/resin
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/resin/resin.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/resin
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/*
%attr(754,root,root) /etc/rc.d/init.d/resin
%attr(755,root,root) %{_bindir}/resin
%dir %{httpdir}/resin
%{httpdir}/resin/webapps
%attr(775,root,http) %dir %{httpdir}/resin/WEB-INF
%{httpdir}/resin/WEB-INF/*
%{_datadir}/resin
%attr(770,root,http) %dir /var/log/resin
%attr(660,root,http) %ghost /var/log/resin/*
%attr(750,root,root) %dir /var/log/archiv/resin
%defattr(660,root,http,0770)
%{_localstatedir}/lib/resin/cache
%{_localstatedir}/lib/resin/work
%{_localstatedir}/lib/resin/war_expand

%files doc
%defattr(644,root,root,755)
%attr(750,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/resin/examples
%{httpdir}/resin

%files mod_caucho
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/mod_caucho.conf
%attr(640,root,http) %config %verify(not md5 mtime size) %{_sysconfdir}/resin/apache2resin.conf
%attr(755,root,root) %{_libexecdir}/mod_caucho.so

%files hardcore
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/resin/libexec/resin.o
