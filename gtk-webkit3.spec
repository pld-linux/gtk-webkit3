# TODO: 
# - optflags
# - review BR and R
# - review configure options
#
# Conditional build:
%bcond_without	introspection	# disable introspection
#
Summary:	Port of WebKit embeddable web component to GTK+
Summary(pl.UTF-8):	Port osadzalnego komponentu WWW WebKit do GTK+
Name:		gtk-webkit3
Version:	1.3.12
Release:	0.1
License:	BSD-like
Group:		X11/Libraries
Source0:	http://webkitgtk.org/webkit-%{version}.tar.gz
# Source0-md5:	f76350682f56761e734faba8689903b5
URL:		http://webkitgtk.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cairo-devel >= 1.6
BuildRequires:	enchant-devel >= 0.22
BuildRequires:	flex >= 2.5.33
BuildRequires:	fontconfig-devel >= 2.4.0
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	geoclue-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.22.0
BuildRequires:	glibc-misc
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 0.9.5}
BuildRequires:	gperf
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.25
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	libicu-devel >= 4.2.1
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsoup-devel >= 2.33.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	libxslt-devel >= 1.1.7
BuildRequires:	pango-devel >= 1:1.12
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
BuildRequires:	xorg-lib-libXft-devel >= 2.0.0
BuildRequires:	xorg-lib-libXt-devel
Requires:	cairo >= 1.6
Requires:	enchant >= 0.22
Requires:	gstreamer-plugins-base >= 0.10.25
Requires:	gtk+2 >= 2:2.20.0
Requires:	libsoup >= 2.30.0
Requires:	libxml2 >= 1:2.6.30
Requires:	libxslt >= 1.1.7
Requires:	pango >= 1:1.12
%{?with_introspection:Conflicts:	gir-repository < 0.6.5-7}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
webkit is a port of the WebKit embeddable web component to GTK+.

%description -l pl.UTF-8
webkit to port osadzalnego komponentu WWW WebKit do GTK+.

%package devel
Summary:	Development files for WebKit
Summary(pl.UTF-8):	Pliki programistyczne WebKit
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel >= 1.6
Requires:	enchant-devel >= 0.22
Requires:	fontconfig-devel >= 2.4.0
Requires:	freetype-devel >= 1:2.1.8
Requires:	geoclue-devel
Requires:	glib2-devel >= 1:2.22.0
Requires:	gstreamer-devel >= 0.10
Requires:	gstreamer-plugins-base-devel >= 0.10.25
Requires:	gtk+2-devel >= 2:2.20.0
Requires:	libicu-devel >= 4.2.1
Requires:	libjpeg-devel
Requires:	libpng-devel
Requires:	libsoup-devel >= 2.30.0
Requires:	libstdc++-devel
Requires:	libxml2-devel >= 1:2.6.30
Requires:	libxslt-devel >= 1.1.7
Requires:	pango-devel >= 1:1.12
Requires:	sqlite3-devel
Requires:	xorg-lib-libXt-devel

%description devel
Development files for WebKit.

%description devel -l pl.UTF-8
Pliki programistyczne WebKit.

%prep
%setup -q -n webkit-%{version}

%build
%{__gtkdocize}
%{__aclocal} -I Source/autotools
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--with-gtk=3.0 \
	--disable-silent-rules \
	--enable-3d-transforms \
	--enable-dom-storage \
	--enable-geolocation \
	--enable-icon-database \
	%{__enable_disable introspection} \
	--enable-video \
	--with-font-backend=freetype

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

: > webkit-3.0.lang
#find_lang webkit-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f webkit-3.0.lang
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_bindir}/jsc-3
%attr(755,root,root) %{_libdir}/libwebkitgtk-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwebkitgtk-3.0.so.0
%if %{with introspection}
%{_libdir}/girepository-1.0/JSCore-3.0.typelib
%{_libdir}/girepository-1.0/WebKit-3.0.typelib
%endif
%dir %{_datadir}/webkit-3.0
%{_datadir}/webkit-3.0/resources
%dir %{_datadir}/webkitgtk-3.0
%{_datadir}/webkitgtk-3.0/images
%{_datadir}/webkitgtk-3.0/webinspector
/usr/share/glib-2.0/schemas/org.webkitgtk-3.0.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwebkitgtk-3.0.so
%{_libdir}/libwebkitgtk-3.0.la
%if %{with introspection}
%{_datadir}/gir-1.0/JSCore-3.0.gir
%{_datadir}/gir-1.0/WebKit-3.0.gir
%endif
%{_includedir}/webkit-3.0
%{_pkgconfigdir}/webkitgtk-3.0.pc