%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A server process which provides boot information to diskless clients
Name:		bootparamd
Version:	0.17
Release:	32
License:	BSD
Group:		System/Servers
Url:		ftp://sunsite.unc.edu/pub/Linux/system/network/netkit
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/netkit/netkit-bootparamd-0.17.tar.gz
Source1:	bootparamd.init
Patch0:		netkit-bootparamd-0.17_rpc_get_myaddress.patch
BuildRequires:	pkgconfig(libtirpc)
Requires(post,preun):	rpm-helper
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
%setup -qn netkit-bootparamd-%{version}
%autopatch -p1

%build
%serverbuild
./configure --prefix=%{_prefix}
sed -i -e '
	s,^CC=*.$,CC=cc,;
	s,-O2,\$(RPM_OPT_FLAGS) -D_BSD_SOURCE,;
	s,^BINDIR=.*$,BINDIR=%{_bindir},;
	s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
	s,^MANDIR=.*$,MANDIR=%{_mandir},;
	' MCONFIG
%make LIBS="-ltirpc"

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

