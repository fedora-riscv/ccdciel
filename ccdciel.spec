%global gittag v0.9.78

Name:           ccdciel
Version:        0.9.78
Release:        %autorelease
Summary:        CCD capture software

License:        GPLv3+
URL:            http://www.ap-i.net/ccdciel/
Source0:        https://github.com/pchev/%{name}/archive/%{gittag}/%{name}-%{version}.tar.gz


# Patch to avoid stripping debuginfo from executable
# Since this is Fedora specific we don't ask upstream to include
Patch100:       ccdciel-0.9.77_fix_debuginfo.patch

ExclusiveArch:  %{fpc_arches}
ExcludeArch:    ppc64le

BuildRequires:  desktop-file-utils
BuildRequires:  fpc
BuildRequires:  lazarus >= 1.6.2
BuildRequires:  libappstream-glib
BuildRequires:  make

# CCDciel requires libpasastro to function properly
# but rpm doesn't find this autorequire
Requires:       libpasastro%{?_isa}
Requires:       libpasraw%{?_isa}

Recommends:     astrometry, astrometry-tycho2
Recommends:     libindi


%description
CCDciel is a free CCD capture software intended for the amateur astronomer. 
It include all the features required to perform digital imaging 
CCD observation of celestial objects.
Using the standard drivers protocol INDI and ASCOM it can connect and control 
the CCD camera, the focuser, the filter wheel and the telescope mount.
It tightly integrates with Skychart to provide telescope control while
Indistarter can be used to control INDI server drivers


%package        doc
Summary:        Documentation files for %{name}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains documentation for %{name}.


%prep
%autosetup -p1

# Make sure we don't use bundled libraries
rm -rf library/*


%build
# Configure script requires non standard parameters
./configure lazarus=%{_libdir}/lazarus prefix=%{_prefix}

# Ccdciel doesn't like parallel building so we don't use macro.
# We pass options to fpc compiler for generate debug info.
make fpcopts="-O1 -gw3 -fPIC"


%install
make install PREFIX=%{buildroot}%{_prefix}

# Copy relevant documentation
cp -p doc/doc_%{name}_en.pdf %{buildroot}%{_pkgdocdir}


%check
# Menu entry
desktop-file-validate %{buildroot}%{_datadir}/applications/net.ap_i.%{name}.desktop

# Appdata file check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/net.ap_i.%{name}.metainfo.xml


%files
%license LICENSE gpl-3.0.txt
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/net.ap_i.%{name}.desktop
%{_datadir}/metainfo/net.ap_i.%{name}.metainfo.xml
%{_datadir}/icons/*/*/*/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/pixmaps/%{name}.png


%files      doc
%{_pkgdocdir}


%changelog
%autochangelog
