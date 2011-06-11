# TODO: 
# - review configure options
#
# Conditional build:
%bcond_without	introspection	# disable introspection
#
Summary:	Port of WebKit embeddable web component to GTK+ 3
Summary(pl.UTF-8):	Port osadzalnego komponentu WWW WebKit do GTK+ 3
Name:		gtk-webkit3
Version:	1.4.0
Release:	1
License:	BSD-like
Group:		X11/Libraries
Source0:	http://webkitgtk.org/webkit-%{version}.tar.gz
# Source0-md5:	10c969db3b5484c71df1aa9a338377ff
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
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	glibc-misc
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 0.10.0}
BuildRequires:	gperf
BuildRequires:	gstreamer-devel >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.25
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	libicu-devel >= 4.2.1
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsoup-devel >= 2.34.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	libxslt-devel >= 1.1.7
BuildRequires:	pango-devel >= 1:1.12
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	xorg-lib-libXft-devel >= 2.0.0
BuildRequires:	xorg-lib-libXt-devel
Requires(post,postun):	glib2 >= 1:2.26.0
Requires:	cairo >= 1.6
Requires:	enchant >= 0.22
Requires:	gstreamer-plugins-base >= 0.10.25
Requires:	gtk+3 >= 3.0.0
Requires:	libsoup >= 2.34.0
Requires:	libxml2 >= 1:2.6.30
Requires:	libxslt >= 1.1.7
Requires:	pango >= 1:1.12
%{?with_introspection:Conflicts:	gir-repository < 0.6.5-7}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
gtk-webkit3 is a port of the WebKit embeddable web component to GTK+ 3.

%description -l pl.UTF-8
gtk-webkit3 to port osadzalnego komponentu WWW WebKit do GTK+ 3.

%package devel
Summary:	Development files for WebKit for GTK+ 3
Summary(pl.UTF-8):	Pliki programistyczne komponentu WebKit dla GTK+ 3
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.28.0
Requires:	gtk+3-devel >= 3.0.0
Requires:	libsoup-devel >= 2.34.0

%description devel
Development files for WebKit for GTK+ 3.

%description devel -l pl.UTF-8
Pliki programistyczne komponentu WebKit dla GTK+ 3.

%prep
%setup -q -n webkit-%{version}

mv Source/WebKit/gtk/po/{gr,el}.po

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I Source/autotools
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules \
	%{__enable_disable introspection} \
	--with-gtk=3.0 \
	--enable-3d-transforms \
	--enable-dom-storage \
	--enable-geolocation \
	--enable-icon-database \
	--enable-video \
	--with-font-backend=freetype

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libwebkitgtk-3.0.la

%find_lang webkit-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas

%postun
/sbin/ldconfig
%glib_compile_schemas

%files -f webkit-3.0.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS
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
%{_datadir}/glib-2.0/schemas/org.webkitgtk-3.0.gschema.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwebkitgtk-3.0.so
%if %{with introspection}
%{_datadir}/gir-1.0/JSCore-3.0.gir
%{_datadir}/gir-1.0/WebKit-3.0.gir
%endif
%{_includedir}/webkit-3.0
%{_pkgconfigdir}/webkitgtk-3.0.pc
