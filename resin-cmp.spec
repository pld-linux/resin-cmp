Summary:	A fast servlet and JSP engine
Name:		resin-cmp
Version:	1.0.1
Release:	3
License:	Caucho Developer Source License
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
URL:		http://www.caucho.com/
Source0:	http://www.caucho.com/download/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}-mod_caucho.conf
Source5: %{name}-conf_resin.conf
Source6: %{name}-conf_apache2resin.conf
Source7: %{name}-conf_browsers.conf
Source8: %{name}-conf_jdbc.conf
Source9: %{name}-conf_ping.conf
Source10: %{name}-conf_sessions.conf
Source11: %{name}-conf_ssl.conf
Source12: %{name}-conf_user-dirs.conf
Source13: %{name}-conf_examples-params.conf
Source14: %{name}-conf_examples-webapps.conf

Patch0:		%{name}-configure-test-httpd.conf.patch
# autoconf 2.5x is not working here
Patch1:		%{name}-configure-libssl_so.patch
Patch2:		%{name}-mod_caucho-ipv6.patch
Patch3:		%{name}-makefile_in-jni_include.patch
# it's known it's better to use apache as http server, but
# resin itself has got httpd too.
Provides:	httpd
Provides:	webserver
Provides:	jsp, servlet, ejb
Conflicts:	resin
# Resin-EJB needs JDK 1.2.
Requires:	ibm-java-sdk >= 1.2
Requires:	sed
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	apache-devel
# to make it consistent with Requires -- ibm-java-sdk conflicts with kaffe
BuildRequires:	ibm-java-sdk >= 1.2 
BuildRequires:	openssl-devel

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

%package doc
Summary:	Additional documentation for Resin
Requires: resin-cmp = %{version}
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery

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

%package mod_caucho
Summary:	Apache module for resin
Requires: resin-cmp = %{version}
Group:		Networking/Daemons
Requires:	apache
Requires:	apache(EAPI)
Prereq:		%{_sbindir}/apxs

%description mod_caucho
Allows to use JSP requests under Apache

%define		_libexecdir	%{_prefix}/lib/apache

%prep 
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure2_13 \
	--with-apache \
	--with-java-home=/usr/lib/java-sdk \
	--with-jni-include=/usr/include/jdk \
	--with-openssl=%{_prefix} \
	--enable-linux-smp

%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libexecdir} \
	  $RPM_BUILD_ROOT%{_sysconfdir}/{httpd,rc.d/init.d,sysconfig} \
	  $RPM_BUILD_ROOT%{_datadir}/resin/{bin,lib,conf/examples,sql,xsl} \
	  $RPM_BUILD_ROOT/home/httpd/resin/webapps \
	  $RPM_BUILD_ROOT/var/{run,log}/resin \
	  $RPM_BUILD_ROOT/var/lib/resin/{cache,work}

cp -R bin lib xsl sql $RPM_BUILD_ROOT%{_datadir}/resin
cp -R doc/*  $RPM_BUILD_ROOT/home/httpd/resin

for conf in %{SOURCE5} %{SOURCE6} %{SOURCE7} %{SOURCE8} %{SOURCE9} \
	%{SOURCE10} %{SOURCE11} %{SOURCE12} ; do
	install $conf \
		$RPM_BUILD_ROOT%{_datadir}/resin/conf/$(basename $conf|sed "s/%{name}-conf_//")
done
for conf in %{SOURCE13} %{SOURCE14} ; do
	install $conf \
		$RPM_BUILD_ROOT%{_datadir}/resin/conf/examples/$(basename $conf|sed "s/%{name}-conf_examples-//")
done

install src/c/plugin/apache/mod_caucho.so $RPM_BUILD_ROOT/%{_libexecdir}
install src/c/plugin/resin/resin $RPM_BUILD_ROOT%{_datadir}/resin/bin
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/resin
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/resin
install %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/mod_caucho.conf

gzip -9nf LICENSE readme.txt conf/*

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/resin ]; then
		/etc/rc.d/init.d/resin stop 1>&2
	fi
	/sbin/chkconfig --del resin
fi
rm -rf /var/lib/resin/cache/*
rm -rf /home/httpd/resin/WEB-INF/{tmp,work}
rm -rf /var/log/resin/*

%post
/sbin/chkconfig --add resin
if [ -f /var/lock/subsys/resin ]; then
	/etc/rc.d/init.d/resin restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/resin start\" to start resin daemon."
fi

%preun mod_caucho
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n caucho %{_libexecdir}/mod_caucho.so 1>&2
	grep -v -q "^Include.*mod_caucho.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%post mod_caucho
%{_sbindir}/apxs -e -a -n caucho %{_libexecdir}/mod_caucho.so 1>&2
if [ -f /etc/httpd/httpd.conf ] && \
	! grep -q "^Include.*mod_caucho.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/mod_caucho.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start httpd daemon."
# it's not very smart solution.. ;-)
fi

%preun doc
echo "Disabling examples in resin.conf"
sed 's/<\(resin:include href="examples.*\)>/<!-- \1 -->/' \
	%{_datadir}/resin/conf/resin.conf > \
	%{_datadir}/resin/conf/resin.conf.tmp
mv %{_datadir}/resin/conf/resin.conf{.tmp,}
if [ -f /var/lock/subsys/resin ]; then
	/etc/rc.d/init.d/resin restart 1>&2
fi

%post doc
echo "Setting permissions to WEB-INF directories"
find /home/httpd/resin -type d -name WEB-INF -exec chown -R root:http {} \; -exec chmod -R g+w {} \;
echo "Enabling examples in resin.conf"
sed 's/<!-- \(resin:include href="examples.*\) -->/<\1>/' \
	%{_datadir}/resin/conf/resin.conf > \
	%{_datadir}/resin/conf/resin.conf.tmp
mv %{_datadir}/resin/conf/resin.conf{.tmp,}
if [ -f /var/lock/subsys/resin ]; then
	/etc/rc.d/init.d/resin restart 1>&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.gz readme.txt.gz conf/*.gz

%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) %{_datadir}/resin/conf/*.conf
%attr(0640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/resin
%attr(0754,root,root) /etc/rc.d/init.d/resin

%dir /home/httpd/resin
/home/httpd/resin/webapps
%attr(0775,root,http) %dir /home/httpd/resin/WEB-INF
/home/httpd/resin/WEB-INF/*

%dir %{_datadir}/resin
%dir %{_datadir}/resin/conf
%dir %{_datadir}/resin/bin
%attr(0755,root,root) %{_datadir}/resin/bin/*
%{_datadir}/resin/lib
%{_datadir}/resin/xsl
%{_datadir}/resin/sql

%defattr(644,http,http,0770)
/var/log/resin
/var/run/resin
/var/lib/resin

%files doc
%defattr(644,root,root,755)
%attr(0640,root,http) %config(noreplace) %verify(not size mtime md5) %{_datadir}/resin/conf/examples
/home/httpd/resin

%files mod_caucho
%defattr(644,root,root,755)
%attr(0640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd/mod_caucho.conf
%attr(0755,root,root) %{_libexecdir}/mod_caucho.so
