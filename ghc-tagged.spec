#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	tagged
Summary:	Haskell 98 phantom types to avoid unsafely passing dummy arguments
Summary(pl.UTF-8):	Typy fantomowe Haskella 98 dla uniknięcia niebezpiecznej analizy zaślepkowych argumentów
Name:		ghc-%{pkgname}
Version:	0.8.6
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/tagged
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	08cebb2c83fba496cc87d859eddb2d7b
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/tagged
BuildRequires:	ghc >= 7.10
BuildRequires:	ghc-base >= 2
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-deepseq >= 1.1
BuildRequires:	ghc-deepseq < 1.5
BuildRequires:	ghc-template-haskell >= 2.8
BuildRequires:	ghc-transformers >= 0.4.2.0
BuildRequires:	ghc-transformers < 0.6
%if %{with prof}
BuildRequires:	ghc-prof >= 7.10
BuildRequires:	ghc-base-prof >= 2
BuildRequires:	ghc-deepseq-prof >= 1.1
BuildRequires:	ghc-template-haskell-prof >= 2.8
BuildRequires:	ghc-transformers-prof >= 0.4.2.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-base >= 2
Requires:	ghc-deepseq >= 1.1
Requires:	ghc-template-haskell >= 2.8
Requires:	ghc-transformers >= 0.4.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Haskell 98 phantom types to avoid unsafely passing dummy arguments.

%description -l pl.UTF-8
Typy fantomowe Haskella 98 dla uniknięcia niebezpiecznej analizy
zaślepkowych argumentów.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 2
Requires:	ghc-deepseq-prof >= 1.1
Requires:	ghc-template-haskell-prof >= 2.8
Requires:	ghc-transformers-prof >= 0.4.2.0

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}
%patch -P0 -p1

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build

runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.markdown LICENSE README.markdown %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Proxy
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Proxy/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Proxy/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Proxy/*.p_hi
%endif
