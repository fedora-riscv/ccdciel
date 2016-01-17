%global svnver 20160105svn
Name:           ccdciel
Version:        0.2.0
Release:        10.%{svnver}%{?dist}
Summary:        CCD capture software

License:        GPLv3+
URL:            http://www.ap-i.net/ccdciel/
# The source code is not available upstream as a package so we pulled it 
# from upstream's vcs. Use the following commands to generate the tarball:
# svn export -r 115 svn://svn.code.sf.net/p/ccdciel/code/trunk ccdciel-0.2.0
# tar -cJvf ccdciel-0.2.0-20160105svn.tar.xz ccdciel-0.2.0
Source0:        %{name}-%{version}-%{svnver}.tar.xz

# Patch to avoid stripping debuginfo from executable
# Since this is Fedora specific we don't ask upstream to include
Patch0:         ccdciel_fix_stripping.patch

# fpc isn't available on aarch64 and s390
# lazarus isn't available on ppc and s390
# so ccdciel could not build
# https://bugzilla.redhat.com/show_bug.cgi?id=###
# (I will open a bug to track this when imported in scm)
ExcludeArch:    aarch64 %{power64} s390 s390x

BuildRequires:  fpc, lazarus desktop-file-utils, libappstream-glib

# CCDciel requires libpasastro to function properly
# but rpm doesn't find this autorequire
Requires:       libpasastro%{?_isa}

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

#Remove spurious executable bit
chmod -x ./component/synapse/source/lib/*.pas

# Fix wrong FSF address in source headers
# asked upstream to fix this
grep -rl '59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.' * | xargs -i@ sed -i 's/59 Temple Place - Suite 330, Boston, MA  02111-1307, USA./51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA./g' @

%build
# Configure script requires non standard parameters
./configure lazarus=%{_libdir}/lazarus prefix=%{_prefix}

# Ccdciel doesn't like parallel building so we don't use macro.
# We pass options to fpc compiler for generate debug info.
make fpcopts="-O1 -g -gl -OoREGVAR -Ch2000000 -CX -XX"

%install
make install PREFIX=%{buildroot}%{_prefix}


%check
# Menu entry
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

# Appdata file check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml

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
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/icons/*/*/*/%{name}.png
%{_datadir}/pixmaps/%{name}.png


%changelog
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