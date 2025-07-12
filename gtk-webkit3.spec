# TODO: review configure options:
# - gamepad
# - battery-status (BR: upower-devel)
#
# Conditional build:
%bcond_without	introspection	# disable introspection
%bcond_without	wayland		# Wayland target
#
# it's not possible to build this with debuginfo on 32bit archs due to
# memory constraints during linking
%ifarch %{ix86} x32
%define		_enable_debug_packages		0
%endif
Summary:	Port of WebKit embeddable web component to GTK+ 3
Summary(pl.UTF-8):	Port osadzalnego komponentu WWW WebKit do GTK+ 3
Name:		gtk-webkit3
# note: for 2.6.x series see gtk-webkit4
Version:	2.4.11
Release:	17
License:	BSD-like
Group:		X11/Libraries
Source0:	http://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz
# Source0-md5:	24a25ccc30a7914ae50922aedf24b7bc
Patch0:		atomic-ops.patch
Patch1:		x32.patch
Patch2:		abs.patch
Patch3:		%{name}-icu59.patch
Patch4:		icu65.patch
Patch5:		glib2.68.patch
Patch6:		icu68.patch
Patch7:		grammar.patch
Patch8:		volatile.patch
Patch9:		libxml2-2.12.patch
Patch10:	c++17.patch
URL:		http://webkitgtk.org/
BuildRequires:	/usr/bin/ld.gold
BuildRequires:	EGL-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	at-spi2-core-devel >= 2.6.0
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	bison >= 1.875
BuildRequires:	cairo-devel >= 1.10
BuildRequires:	enchant-devel >= 0.22
BuildRequires:	flex >= 2.5.33
BuildRequires:	fontconfig-devel >= 2.5.0
BuildRequires:	freetype-devel >= 1:2.1.8
BuildRequires:	gcc-c++ >= 6:4.7
BuildRequires:	geoclue2-devel >= 2.1.5
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	glibc-misc
%{?with_introspection:BuildRequires:	gobject-introspection-devel >= 1.32.0}
BuildRequires:	gperf
BuildRequires:	gstreamer-devel >= 1.0.3
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.3
# GTK+ 2.x for webkit2 plugin process; GTK+ 3 for base GUI
BuildRequires:	gtk+2-devel >= 2:2.24.10
BuildRequires:	gtk+3-devel >= 3.10.0
BuildRequires:	gtk-doc >= 1.10
BuildRequires:	harfbuzz-devel >= 0.9.7
BuildRequires:	harfbuzz-icu-devel >= 0.9.7
%ifarch i386 i486
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libicu-devel >= 59
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsecret-devel
BuildRequires:	libsoup-devel >= 2.42.0
BuildRequires:	libstdc++-devel >= 6:7
# libtool with -fuse-ld= gcc option support
BuildRequires:	libtool >= 2:2.4.2-13
BuildRequires:	libwebp-devel
BuildRequires:	libxml2-devel >= 1:2.6.30
BuildRequires:	libxslt-devel >= 1.1.7
BuildRequires:	pango-devel >= 1:1.32.0
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	ruby
BuildRequires:	sqlite3-devel >= 3
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	cairo >= 1.10
Requires:	enchant >= 0.22
Requires:	fontconfig-libs >= 2.5.0
Requires:	freetype >= 1:2.1.8
Requires:	glib2 >= 1:2.36.0
Requires:	gstreamer >= 1.0.3
Requires:	gstreamer-plugins-base >= 1.0.3
Requires:	gtk+2 >= 2:2.24.10
Requires:	gtk+3 >= 3.10.0
Requires:	harfbuzz >= 0.9.7
Requires:	libsoup >= 2.42.0
Requires:	libxml2 >= 1:2.6.30
Requires:	libxslt >= 1.1.7
Requires:	pango >= 1:1.32.0
%{?with_introspection:Conflicts:	gir-repository < 0.6.5-7}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# __once_call, __once_called non-function symbols from libstdc++
%define		skip_post_check_so	lib.*gtk-3.0.*

# JSStringRef uses "!this" comparisons (UB)
%define		specflags	-fno-delete-null-pointer-checks

%description
gtk-webkit3 is a port of the WebKit embeddable web component to GTK+
3.

%description -l pl.UTF-8
gtk-webkit3 to port osadzalnego komponentu WWW WebKit do GTK+ 3.

%package devel
Summary:	Development files for WebKit for GTK+ 3
Summary(pl.UTF-8):	Pliki programistyczne komponentu WebKit dla GTK+ 3
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0
Requires:	gtk+3-devel >= 3.10.0
Requires:	libsoup-devel >= 2.42.0
Requires:	libstdc++-devel >= 6:7

%description devel
Development files for WebKit for GTK+ 3.

%description devel -l pl.UTF-8
Pliki programistyczne komponentu WebKit dla GTK+ 3.

%package apidocs
Summary:	WebKit API documentation
Summary(pl.UTF-8):	Dokumentacja API WebKita
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
WebKit API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API WebKita.

%prep
%setup -q -n webkitgtk-%{version}
%ifarch i386 i486
%patch -P0 -p1
%endif
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1

%build
%{__libtoolize}
%{__aclocal} -I Source/autotools
%{__autoconf}
%{__autoheader}
%{__automake}
CXXFLAGS="%{rpmcxxflags} -fno-delete-null-pointer-checks -Wno-expansion-to-defined"
%configure \
%ifarch %{x8664}
	LDFLAGS="%{rpmldflags} -fuse-ld=gold" \
%else
	LDFLAGS="%{rpmldflags} -fuse-ld=bfd -Wl,--no-keep-memory" \
%endif
	--disable-gtk-doc \
	--disable-silent-rules \
	--enable-geolocation \
	--enable-glx \
	%{__enable_disable introspection} \
	%{!?with_wayland:--disable-wayland-target} \
	--enable-webgl \
	--with-gtk=3.0 \
	--with-html-dir=%{_gtkdocdir}

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/webkit2gtk-3.0/injected-bundle/*.la

%find_lang WebKitGTK-3.0

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f WebKitGTK-3.0.lang
%defattr(644,root,root,755)
%doc ChangeLog NEWS
%attr(755,root,root) %{_bindir}/jsc-3
%attr(755,root,root) %{_libexecdir}/WebKitNetworkProcess
%attr(755,root,root) %{_libexecdir}/WebKitPluginProcess
%attr(755,root,root) %{_libexecdir}/WebKitWebProcess
%attr(755,root,root) %{_libdir}/libwebkitgtk-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwebkitgtk-3.0.so.0
%attr(755,root,root) %{_libdir}/libwebkit2gtk-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwebkit2gtk-3.0.so.25
%attr(755,root,root) %{_libdir}/libjavascriptcoregtk-3.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjavascriptcoregtk-3.0.so.0
%if %{with introspection}
%{_libdir}/girepository-1.0/JavaScriptCore-3.0.typelib
%{_libdir}/girepository-1.0/WebKit-3.0.typelib
%{_libdir}/girepository-1.0/WebKit2-3.0.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-3.0.typelib
%endif
%dir %{_libdir}/webkit2gtk-3.0
%dir %{_libdir}/webkit2gtk-3.0/injected-bundle
%attr(755,root,root) %{_libdir}/webkit2gtk-3.0/injected-bundle/libwebkit2gtkinjectedbundle.so
%dir %{_datadir}/webkitgtk-3.0
%{_datadir}/webkitgtk-3.0/images
%{_datadir}/webkitgtk-3.0/resources

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwebkitgtk-3.0.so
%attr(755,root,root) %{_libdir}/libwebkit2gtk-3.0.so
%attr(755,root,root) %{_libdir}/libjavascriptcoregtk-3.0.so
%if %{with introspection}
%{_datadir}/gir-1.0/JavaScriptCore-3.0.gir
%{_datadir}/gir-1.0/WebKit-3.0.gir
%{_datadir}/gir-1.0/WebKit2-3.0.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-3.0.gir
%endif
%{_includedir}/webkitgtk-3.0
%{_pkgconfigdir}/javascriptcoregtk-3.0.pc
%{_pkgconfigdir}/webkitgtk-3.0.pc
%{_pkgconfigdir}/webkit2gtk-3.0.pc
%{_pkgconfigdir}/webkit2gtk-web-extension-3.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/webkitgtk
%{_gtkdocdir}/webkit2gtk
%{_gtkdocdir}/webkitdomgtk
