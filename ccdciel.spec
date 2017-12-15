%global svnversion 748

Name:           ccdciel
Version:        0.9.22
Release:        1.%{svnversion}svn%{?dist}
Summary:        CCD capture software

License:        GPLv3+
URL:            http://www.ap-i.net/ccdciel/
# The source code is not available upstream as a package so we pulled it 
# from upstream's vcs. Use the following commands to generate the tarball:
# svn export -r 748 svn://svn.code.sf.net/p/ccdciel/code/trunk ccdciel-0.9.22
# tar -cJvf ccdciel-0.9.22-748.tar.xz ccdciel-0.9.22
Source0:        %{name}-%{version}-%{svnversion}.tar.xz

# Patch to avoid stripping debuginfo from executable
# Since this is Fedora specific we don't ask upstream to include
Patch0:         ccdciel-0.9.0_fix_stripping.patch

ExclusiveArch:  %{fpc_arches}
# fpc is available on ppc64, but lazarus has some limitations that
# prevents this package to build
ExcludeArch:    ppc64

BuildRequires:  desktop-file-utils
BuildRequires:  fpc
BuildRequires:  lazarus >= 1.6.2
BuildRequires:  libappstream-glib

# CCDciel requires libpasastro to function properly
# but rpm doesn't find this autorequire
Requires:       libpasastro%{?_isa}

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

%prep
%autosetup -p1


%build
# Configure script requires non standard parameters
./configure lazarus=%{_libdir}/lazarus prefix=%{_prefix}

# Ccdciel doesn't like parallel building so we don't use macro.
# We pass options to fpc compiler for generate debug info.
make fpcopts="-O1 -gw3 -fPIC"

%install
make install PREFIX=%{buildroot}%{_prefix}


%check
# Menu entry
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

# Appdata file check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE gpl-3.0.txt
%doc %{_datadir}/doc/%{name}/
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml
%{_datadir}/icons/*/*/*/%{name}.png
%{_datadir}/pixmaps/%{name}.png


%changelog
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
