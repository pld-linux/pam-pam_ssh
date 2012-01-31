Summary:	PAM module for use with SSH keys and ssh-agent
Name:		pam-pam_ssh
Version:	1.97
Release:	2
License:	BSD
Group:		Base
URL:		http://sourceforge.net/projects/pam-ssh/
Source0:	http://downloads.sourceforge.net/pam-ssh/pam_ssh-%{version}.tar.bz2
# Source0-md5:	ef114d67b4951c88a62893437f850784
Source1:	%{name}.tmpfiles
Patch0:		var_run.patch
BuildRequires:	libtool
BuildRequires:	openssh-clients
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
Requires:	openssh-clients
Conflicts:	selinux-policy-targeted < 3.0.8-55
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This PAM module provides single sign-on behavior for UNIX using SSH
keys. Users are authenticated by decrypting their SSH private keys
with the password provided. In the first PAM login session phase, an
ssh-agent process is started and keys are added. The same agent is
used for the following PAM sessions. In any case the appropriate
environment variables are set in the session phase.

%prep
%setup -q -n pam_ssh-%{version}
%patch0 -p1

cat >>pam_ssh.sym <<EOF
pam_sm_acct_mgmt
pam_sm_authenticate
pam_sm_chauthtok
pam_sm_close_session
pam_sm_open_session
pam_sm_setcred
EOF

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-pam-dir=/%{_lib}/security

%{__make} -j1 \
	CPPFLAGS=-I/usr/include/security \
	LDFLAGS="-export-symbols pam_ssh.sym"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/run/pam_ssh \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	INSTALL="install -p" \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/pam_ssh.conf

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README ChangeLog TODO COPYING
%attr(755,root,root) /%{_lib}/security/pam_ssh.so
%{_mandir}/man8/pam_ssh.8*
%ghost %dir %{_localstatedir}/run/pam_ssh
/usr/lib/tmpfiles.d/pam_ssh.conf
