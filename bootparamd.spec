%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A server process which provides boot information to diskless clients
Name:		bootparamd
Version:	0.17
Release:	21
License:	BSD
Group:		System/Servers
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/netkit/netkit-bootparamd-0.17.tar.bz2
Source1:	bootparamd.init
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires:	rpcbind

%description
The bootparamd process provides bootparamd, a server process which
provides the information needed by diskless clients in order for them
to successfully boot.  Bootparamd looks first in /etc/bootparams for an
entry for that particular client; if a local bootparams file doesn't
exist, it looks at the appropriate Network Information Service (NIS)
map.  Some network boot loaders (notably Sun's) rely on special boot
server code on the server, in addition to the rarp and tftp servers.
This bootparamd server process is compatible with SunOS bootparam clients
and servers which need that boot server code.

You should install bootparamd if you need to provide boot information to
diskless clients on your network.

%prep
%setup -q -n netkit-bootparamd-%{version}

%build
%serverbuild
./configure --prefix=%{_prefix}
perl -pi -e '
	s,^CC=*.$,CC=cc,;
	s,-O2,\$(RPM_OPT_FLAGS) -D_BSD_SOURCE,;
	s,^BINDIR=.*$,BINDIR=%{_bindir},;
	s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
	s,^MANDIR=.*$,MANDIR=%{_mandir},;
	' MCONFIG
%make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man{1,5,8}
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
make INSTALLROOT=%{buildroot} install
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/bootparamd

cd %{buildroot}%{_mandir}/man8
ln -s rpc.bootparamd.8.bz2 %{buildroot}%{_mandir}/man8/bootparamd.8.bz2

%post
%_post_service bootparamd

%preun
%_preun_service bootparamd

%files
%{_sbindir}/rpc.bootparamd
%{_bindir}/callbootd
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/rc.d/init.d/bootparamd



%changelog
* Tue May 03 2011 Funda Wang <fwang@mandriva.org> 0.17-18mdv2011.0
+ Revision: 663774
- fix install

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-17mdv2011.0
+ Revision: 603765
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.17-16mdv2010.1
+ Revision: 522257
- rebuilt for 2010.1

* Sun Jul 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.17-15mdv2010.0
+ Revision: 400401
- fix dependencies

* Fri Mar 06 2009 Antoine Ginies <aginies@mandriva.com> 0.17-14mdv2009.1
+ Revision: 350212
- 2009.1 rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0.17-13mdv2009.0
+ Revision: 220490
- rebuild

* Thu Jan 24 2008 Oden Eriksson <oeriksson@mandriva.com> 0.17-12mdv2008.1
+ Revision: 157352
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild with fixed %%serverbuild macro

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 0.17-9mdv2008.1
+ Revision: 135856
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri May 12 2006 Stefan van der Eijk <stefan@eijk.nu> 0.17-9mdk
- rebuild for sparc

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.17-8mdk
- Rebuild

* Thu Aug 11 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.17-7mdk
- fix rpmlint errors (PreReq)

* Thu Aug 11 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.17-6mdk
- fix rpmlint errors (PreReq)

* Wed Jul 16 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.17-5mdk
- cleanups
- s/Copyright/License/
- fix unpackaged files
- prereq on rpm-helper

