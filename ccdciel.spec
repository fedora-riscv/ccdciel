%global gittag v0.9.73

Name:           ccdciel
Version:        0.9.73
Release:        2%{?dist}
Summary:        CCD capture software

License:        GPLv3+
URL:            http://www.ap-i.net/ccdciel/
Source0:        https://github.com/pchev/%{name}/archive/%{gittag}/%{name}-%{version}.tar.gz


# Patch to avoid stripping debuginfo from executable
# Since this is Fedora specific we don't ask upstream to include
Patch100:       ccdciel-0.9.55_fix_debuginfo.patch

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
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

# Appdata file check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml


%files
%license LICENSE gpl-3.0.txt
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/icons/*/*/*/%{name}.png
%{_datadir}/pixmaps/%{name}.png


%files      doc
%{_pkgdocdir}


%changelog
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 04 2020 Mattia Verga <mattia.verga@protonmail.com> - 0.9.73-1
- Update to 0.9.73
- Add make to BuildRequires
- Split documentation package

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.68-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 18 2020 Mattia Verga <mattia.verga@protonmail.com> - 0.9.68-3
- Add libpasraw to Requires

* Sat Feb 08 2020 Mattia Verga <mattia.verga@protonmail.com> - 0.9.68-2
- ExcludeArch ppc64le due to compilation errors

* Sat Feb 01 2020 Mattia Verga <mattia.verga@protonmail.com> - 0.9.68-1
- Update to 0.9.68

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Mattia Verga <mattia.verga@protonmail.com> - 0.9.65-1
- Update to 0.9.65

* Thu Aug 29 2019 Mattia Verga <mattia.verga@protonmail.com> - 0.9.60-1
- Update to 0.9.60

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Apr 20 2019 Mattia Verga <mattia.verga@protonmail.com> - 0.9.55-1
- Update to 0.9.55

* Sat Feb 09 2019 Mattia Verga <mattia.verga@protonmail.com> - 0.9.52-1
- Update to 0.9.52

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 11 2018 Mattia Verga <mattia.verga@protonmail.com> - 0.9.47-1
- Update to 0.9.47

* Sun Jul 15 2018 Mattia Verga <mattia.verga@yandex.com> - 0.9.41-1
- Update to 0.9.41

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 05 2018 Mattia Verga <mattia.verga@email.it> - 0.9.38-1
- Update to 0.9.38

* Fri Apr 20 2018 Mattia Verga <mattia.verga@email.it> - 0.9.35-1
- Update to 0.9.35

* Sun Mar 11 2018 Mattia Verga <mattia.verga@email.it> - 0.9.29-1
- Update to 0.9.29
- Sources moved to github

* Sun Feb 25 2018 Mattia Verga <mattia.verga@email.it> - 0.9.26-1.816svn
- Update to 0.9.26 rev816

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.22-3.748svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.22-2.748svn
- Remove obsolete scriptlets

* Fri Dec 15 2017 Mattia Verga <mattia.verga@email.it> - 0.9.22-1.748svn
- Update to 0.9.22 rev748

* Sun Dec 03 2017 Mattia Verga <mattia.verga@email.it> - 0.9.18-1.711svn
- Update to 0.9.18 rev711

* Sun Nov 19 2017 Mattia Verga <mattia.verga@email.it> - 0.9.14-1.656svn
- Update to 0.9.14 rev656
- Appdata files moved in metainfo directory

* Wed Nov 01 2017 Mattia Verga <mattia.verga@email.it> - 0.9.11-1.605svn
- Update to 0.9.11 rev605

* Sun Oct 08 2017 Mattia Verga <mattia.verga@email.it> - 0.9.8-1.556svn
- Update to 0.9.8 rev556

* Tue Oct 03 2017 Mattia Verga <mattia.verga@email.it> - 0.9.6-1.533svn
- Update to 0.9.6 rev533

* Sat Sep 23 2017 Mattia Verga <mattia.verga@email.it> - 0.9.4-1.494svn
- Update to 0.9.4 rev494

* Thu Sep 14 2017 Mattia Verga <mattia.verga@email.it> - 0.9.2-1.475svn
- Update to 0.9.2 rev475
- Add astrometry and astrometry-tycho2 as weak dependencies

* Sun Sep 03 2017 Mattia Verga <mattia.verga@email.it> - 0.9.0-1.428svn
- Update to 0.9.0 rev428

* Fri Aug 11 2017 Mattia Verga <mattia.verga@email.it> - 0.8.18-1.417svn
- Update to 0.8.18 rev417

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.16-4.400svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sat Jul 29 2017 Mattia Verga <mattia.verga@email.it> - 0.8.16-3.400svn
- Change FPC build options to fix debug package build

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.16-2.400svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 06 2017 Mattia Verga <mattia.verga@email.it> - 0.8.16-1.400svn
- Update to 0.8.16 rev400

* Sat Jul 01 2017 Mattia Verga <mattia.verga@email.it> - 0.8.15-1.393svn
- Update to 0.8.15 rev393

* Sat May 13 2017 Mattia Verga <mattia.verga@tiscali.it> - 0.8.14-1.382svn
- Update to 0.8.14 rev382

* Mon May 01 2017 Mattia Verga <mattia.verga@tiscali.it> - 0.8.12-1.370svn
- Update to 0.8.12 rev370

* Fri Apr 14 2017 Mattia Verga <mattia.verga@tiscali.it> - 0.8.11-1.351svn
- Update to 0.8.11 rev351

* Tue Mar 28 2017 Mattia Verga <mattia.verga@tiscali.it> - 0.8.8-1.338svn
- Update to 0.8.8 rev338

* Sun Feb 12 2017 Mattia Verga <mattia.verga@tiscali.it> - 0.8.7-3.325svn
- Set ExcludeArch ppc64 due to lazarus limitations

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-2.325svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Mattia Verga <mattia.verga@tiscali.it> - 0.8.7-1.325svn
- Update to 0.8.7

* Sun Jan 15 2017 Mattia Verga <mattia.verga@tiscali.it> - 0.8.6-1.321svn
- Update to 0.8.6

* Wed Dec 21 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.8.5-1.315svn
- Update to 0.8.5

* Tue Sep 27 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.8.4-1.290svn
- Update to 0.8.4

* Fri Sep 23 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.8.3-1.282svn
- Update to 0.8.3

* Sun Sep 04 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.7.2-1.228svn
- Update to 0.7.2

* Tue Aug 16 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.6.2-1.187svn
- Update to 0.6.2

* Sun May 22 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.5.0-1.143svn
- Update to 0.5.0

* Sat May 14 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.4.0-1.131svn
- Update to 0.4.0
- Use new fpc_arches macro as ExclusiveArch

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2.20160120svn124
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.3.0-1.20160120svn124
- Update to 0.3.0
- FSF address is now fixed upstream

* Sat Jan 16 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-10.20160105svn
- Moved tests into %%check
- Added architecture to libpasastro dependency
- Fixed wrong FSF address in sources (and reported upstream)

* Tue Jan 05 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-9.20160105svn
- Update svn revision

* Sun Jan 03 2016 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-8.20151220svn
- Set fpc build options from make command instead of patching sources

* Sun Dec 20 2015 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-7.20151220svn
- Properly set ExcludeArch

* Sun Dec 20 2015 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-6.20151220svn
- Libraries are now in separate package libpasastro

* Tue Dec 15 2015 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-4.20151214svn
- Disable build on s390, aarch64 and ppc

* Mon Dec 14 2015 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-3.20151214svn
- Update svn version to fix compatibility with lazarus 1.6

* Wed Dec 09 2015 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-2.20151209svn
- Removed license text as separate source
- Fix license to be GPLv3+

* Wed Dec 09 2015 Mattia Verga <mattia.verga@tiscali.it> - 0.2.0-1.20151209svn
- Initial release
