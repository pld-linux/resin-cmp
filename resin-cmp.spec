Summary:	A fast servlet and JSP engine
Summary(pl):	Szybki silnik servletów i JSP
Name:		resin-cmp
Version:	1.0.4
Release:	1
License:	Caucho Developer Source License
Group:		Networking/Daemons/Java
Source0:	http://www.caucho.com/download/%{name}-%{version}.tar.gz
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

# it's known it's better to use apache as http server, but
# resin itself has got httpd too.
Provides:	httpd
Provides:	webserver
Provides:	jsp, servlet, ejb
Conflicts:	resin
Requires:	jdk >= 1.2
Requires:	sed
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	jdk >= 1.2
BuildRequires:	openssl-devel
BuildRequires:	autoconf >= 1.4
BuildRequires:	automake >= 1.4d
BuildRequires:	libtool >= 1.4


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
generowaæ prosy XML i u¿ywaæ filtra XSL do formatowania wyników
zale¿nie od mo¿liwo¶ci klienta, od Palm Pilotów do Mozilli.

%package doc
Summary:	Additional documentation for Resin
Summary(pl):	Dodatkowa dokumentacja do Resina
Requires:	resin-cmp = %{version}
Group:		Networking/Daemons/Java

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
  pod uniksem, z Apache pod Win32, IIS, O'Reilly WebSite, Netscape.
- podstawowy resin.conf: konfiguracja servletów, konfiguracja bazy
  danych, konfiguracja aplikacji webowych, konfiguracja HTTP i srun,
  ogólna konfiguracja Resina
- przyk³ad servletu, wirtualnych hostów, cachowania, load balancingu
- przewodnik, JavaDoc.

%package mod_caucho
Summary:	Resin module for Apache
Summary(pl):	Modu³ Resina dla Apache
Requires:	resin-cmp = %{version}
Group:		Networking/Daemons
Requires:	apache
Requires:	apache(EAPI)
BuildRequires:	apache-devel
Prereq:		%{_sbindir}/apxs

%description mod_caucho
Allows to serve JSP requests under Apache.

%description mod_caucho -l pl
Pozwala obs³ugiwaæ ¿±dania JSP spod Apache.

%package hardcore
Summary:	Resin kernel module
Summary(pl):	Modu³ j±dra do Resina
Requires:	resin-cmp = %{version}
Group:		Networking/Daemons
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

%define		_libexecdir	%{_prefix}/lib/apache

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
aclocal
%{__autoconf}
%configure \
	--with-apache \
	--with-apache-eapi \
	--with-java-home=%{_libdir}/java-sdk \
	--with-jni-include=%{_includedir}/jdk \
	--with-openssl=%{_prefix} \
	--enable-linux-smp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libexecdir} \
	  $RPM_BUILD_ROOT%{_sysconfdir}/{resin/examples,rc.d/init.d,sysconfig} \
	  $RPM_BUILD_ROOT%{_sysconfdir}/{logrotate.d,httpd} \
	  $RPM_BUILD_ROOT%{_datadir}/resin/{lib,sql,xsl,libexec} \
	  $RPM_BUILD_ROOT/home/httpd/resin/webapps \
	  $RPM_BUILD_ROOT%{_localstatedir}/{run,log,log/archiv}/resin \
	  $RPM_BUILD_ROOT%{_localstatedir}/lib/resin/{cache,work,war_expand} \
	  $RPM_BUILD_ROOT/%{_bindir}

cp -R bin lib xsl sql $RPM_BUILD_ROOT%{_datadir}/resin
cp -R doc/*  $RPM_BUILD_ROOT/home/httpd/resin
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

install src/c/plugin/apache/mod_caucho.so $RPM_BUILD_ROOT/%{_libexecdir}
install src/c/plugin/resin/resin $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/resin
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/resin
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d

touch $RPM_BUILD_ROOT/var/log/resin/{access,error,stdout,sterr}_log

gzip -9nf LICENSE readme.txt conf/*

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_localstatedir}/lock/subsys/resin ]; then
		/etc/rc.d/init.d/resin stop 1>&2
	fi
	/sbin/chkconfig --del resin
fi
rm -rf %{_localstatedir}/lib/resin/cache/*
rm -rf /home/httpd/resin/WEB-INF/{tmp,work}

%post
/sbin/chkconfig --add resin
if [ -f %{_localstatedir}/lock/subsys/resin ]; then
	/etc/rc.d/init.d/resin restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/resin start\" to start resin daemon."
fi

%preun mod_caucho
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n caucho %{_libexecdir}/mod_caucho.so 1>&2
	grep -v "^Include.*mod_caucho.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f %{_localstatedir}/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
	echo "You may want to disable apache2resin.conf in resin.conf"
fi

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

%preun doc
echo "Don't forget to disable examples in resin.conf and restart resin-cmp"

%post doc
echo "Setting permissions to WEB-INF directories"
find /home/httpd/resin -type d -name WEB-INF -exec chown -R root:http {} \; -exec chmod -R g+w {} \;
echo "Don't forget to uncomment examples in resin.conf and restart resin-cmp"

%files
%defattr(644,root,root,755)
%doc LICENSE.gz readme.txt.gz conf/*.gz

%attr(0750,root,http) %dir %{_sysconfdir}/resin
%attr(0640,root,http) %config %verify(not size mtime md5) %{_sysconfdir}/resin/resin.conf
%attr(0640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/sysconfig/resin
%attr(0750,root,root) %{_sysconfdir}/logrotate.d

%attr(0754,root,root) /etc/rc.d/init.d/resin
%attr(0755,root,root) %{_bindir}/resin

%dir /home/httpd/resin
/home/httpd/resin/webapps
%attr(0775,root,http) %dir /home/httpd/resin/WEB-INF
/home/httpd/resin/WEB-INF/*
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
%attr(0750,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/resin/examples
/home/httpd/resin

%files mod_caucho
%defattr(644,root,root,755)
%attr(0640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/mod_caucho.conf
%attr(0640,root,http) %config %verify(not size mtime md5) %{_sysconfdir}/resin/apache2resin.conf
%attr(0755,root,root) %{_libexecdir}/mod_caucho.so

%files hardcore
%defattr(644,root,root,755)
%attr(0755,root,root) %{_datadir}/resin/libexec/resin.o
