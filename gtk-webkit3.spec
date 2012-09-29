# TODO: review configure options:
# - accelerated-compositing, notifications, gamepad, dom-mutation-observers, input-color, media-source, media-stream, mhtml, web-audio, web-timing, touch-icon-loading, register-protocol-handler
# - directory-upload
# - webkit2
# - APIs: page-visibility-api, indexed-database, input-speech, image-resizer, quota, animation-api
# - HTML5: microdata, datagrid, data-transfer-items, video-track, file-system, style-scoped
#
# Conditional build:
%bcond_without	introspection	# disable introspection
#
Summary:	Port of WebKit embeddable web component to GTK+ 3
Summary(pl.UTF-8):	Port osadzalnego komponentu WWW WebKit do GTK+ 3
Name:		gtk-webkit3
Version:	1.10.0
Release:	1
License:	BSD-like
Group:		X11/Libraries
Source0:	http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz
# Source0-md5:	6da450ec7793c0a7873d8c8c2cae4eb8
URL:		http://webkitgtk.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	at-spi2-core-devel >= 2.2.1
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	bison >= 1.875
BuildRequires:	cairo-devel >= 1.10
BuildRequires:	enchant-devel >= 0.22
BuildRequires:	flex >= 2.5.33
BuildRequires:	fontconfig-devel >= 2.4.0
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	geoclue-devel
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	glibc-misc
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 0.10.0}
BuildRequires:	gperf
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.4.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	libicu-devel >= 4.2.1
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsoup-devel >= 2.40.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	libxslt-devel >= 1.1.7
BuildRequires:	pango-devel >= 1:1.21.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	sqlite3-devel >= 3.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	cairo >= 1.10
Requires:	enchant >= 0.22
Requires:	glib2 >= 1:2.32.0
Requires:	gstreamer >= 1.0.0
Requires:	gstreamer-plugins-base >= 1.0.0
Requires:	gtk+3 >= 3.4.0
Requires:	libsoup >= 2.40.0
Requires:	libxml2 >= 1:2.6.30
Requires:	libxslt >= 1.1.7
Requires:	pango >= 1:1.21.0
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
Requires:	glib2-devel >= 1:2.32.0
Requires:	gtk+3-devel >= 3.4.0
Requires:	libsoup-devel >= 2.40.0

%description devel
Development files for WebKit for GTK+ 3.

%description devel -l pl.UTF-8
Pliki programistyczne komponentu WebKit dla GTK+ 3.

%package apidocs
Summary:	WebKit API documentation
Summary(pl.UTF-8):	Dokumentacja API WebKita
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
WebKit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API WebKita.

%prep
%setup -q -n webkitgtk-%{version}

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
	--with-gstreamer=1.0 \
	--with-gtk=3.0 \
	--enable-geolocation \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%find_lang webkitgtk-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f webkitgtk-3.0.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS
%attr(755,root,root) %{_bindir}/jsc-3
%attr(755,root,root) %{_libexecdir}/WebKitPluginProcess
%attr(755,root,root) %{_libexecdir}/WebKitWebProcess
%attr(755,root,root) %{_libdir}/libwebkitgtk-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwebkitgtk-3.0.so.0
%attr(755,root,root) %{_libdir}/libwebkit2gtk-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwebkit2gtk-3.0.so.18
%attr(755,root,root) %{_libdir}/libjavascriptcoregtk-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjavascriptcoregtk-3.0.so.0
%if %{with introspection}
%{_libdir}/girepository-1.0/JSCore-3.0.typelib
%{_libdir}/girepository-1.0/WebKit-3.0.typelib
%endif
%dir %{_datadir}/webkitgtk-3.0
%{_datadir}/webkitgtk-3.0/images
%{_datadir}/webkitgtk-3.0/resources
%{_datadir}/webkitgtk-3.0/webinspector

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwebkitgtk-3.0.so
%attr(755,root,root) %{_libdir}/libwebkit2gtk-3.0.so
%attr(755,root,root) %{_libdir}/libjavascriptcoregtk-3.0.so
%if %{with introspection}
%{_datadir}/gir-1.0/JSCore-3.0.gir
%{_datadir}/gir-1.0/WebKit-3.0.gir
%endif
%{_includedir}/webkitgtk-3.0
%{_pkgconfigdir}/webkitgtk-3.0.pc
%{_pkgconfigdir}/webkit2gtk-3.0.pc
%{_pkgconfigdir}/javascriptcoregtk-3.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/webkitgtk
%{_gtkdocdir}/webkit2gtk
