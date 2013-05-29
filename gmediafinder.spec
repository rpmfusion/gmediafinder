%global gitrev 26f89cf

Name:           gmediafinder
Version:        1.5.1
Release:        2.%{gitrev}%{?dist}
Summary:        A program to stream an/or download files
License:        GPLv2
Group:          Applications/Internet
URL:            http://gnomefiles.org/content/show.php/Gmediafinder?content=138588
# Translation:
# https://www.transifex.net/projects/p/gmf/resource/gmediafinderpot/

# checkout instructions
# git clone git://github.com/smolleyes/gmediafinder2.git gmediafinder
# cd gmediafinder
# git rev-parse --short HEAD
# git archive --format=tar --prefix=gmediafinder/ %{gitrev} \
#   -o gmediafinder-%{version}-%{gitrev}.tar
# tar --delete --file=gmediafinder-%{version}-%{gitrev}.tar \
#   gmediafinder/win32
# bzip2 gmediafinder-%{version}-%{gitrev}.tar

Source0:        %{name}-%{version}-%{gitrev}.tar.bz2
BuildArch:      noarch

BuildRequires:  hicolor-icon-theme
BuildRequires:  python-mechanize
BuildRequires:  python-setuptools
BuildRequires:  python-distutils-extra
BuildRequires:  intltool
Requires:       gnome-icon-theme
Requires:       gstreamer-ffmpeg
Requires:       gstreamer-python
Requires:       gstreamer-plugins-bad
Requires:       gstreamer-plugins-base
Requires:       gstreamer-plugins-good
Requires:       pygtk2
Requires:       python-BeautifulSoup
Requires:       python-gdata 
Requires:       python-distutils-extra
Requires:       python-mechanize
Requires:       python-virtkey
Requires:       python-configobj
Requires:       pywebkitgtk
Requires:       pygtk2-libglade
Requires:       projectM-libvisual
Requires:       hicolor-icon-theme


%description
Gmediafinder is a GTK application to stream or download videos and music
from various YouTube-like sites without having flash installed.

%prep
%setup -q -n %{name}

# delete unused directories and files
find -name .git -type d -or -name debian -type d -or -name win32 -type d | xargs rm -rfv

%build
python setup.py build

%install
python setup.py install --root=%{buildroot} 
cp -R data/img/throbber.png %{buildroot}%{_datadir}/%{name}/

# reported upstream
# https://github.com/smolleyes/gmediafinder2/issues/2
chmod a+x %{buildroot}/usr/share/gmediafinder/scripts/get_stream.py
for file in %{buildroot}%{python_sitelib}/GmediaFinder/{lib/checklinks,lib/engines/__init__,lib/get_stream,__init__,lib/downloads/__init__,lib/Translation,lib/__init__,lib/engines/main,lib/player/__init__,gmediafinder,lib/pykey,lib/engines/Youtube/__init__}.py; do
    chmod a+x $file
done

%find_lang %{name}

%post
update-desktop-database -q %{_datadir}/applications &> /dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
   /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun
update-desktop-database -q %{_datadir}/applications &> /dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
   /usr/bin/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
fi

%files -f %{name}.lang
%doc CHANGELOG gpl-2.0.txt README VERSION
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{python_sitelib}/*/* 
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/pyshared/GmediaFinder
%dir %{_datadir}/pyshared

%changelog
* Wed May 29 2013 Martin Gansser <linux4martin@gmx.de> 1.5.1-2.26f89cf
- removed %%desktop-file-validate
- make Youtube engine file executable
- removed  unnecessary requirement python-xlib

* Wed May 29 2013 Martin Gansser <linux4martin@gmx.de> 1.5.1-1.26f89cf
- rebuild for new release

* Sun May 12 2013 Martin Gansser <linux4martin@gmx.de> 1.0.5-1.44eec93
- added python-xlib requirement
- rebuild for new release

* Wed Oct 31 2012 Martin Gansser <linux4martin@gmx.de> 1.0.4-4.302a1a0
- added pyshared as separate %%dir
- added %%gitrev in %%changelog revision

* Tue Oct 30 2012 Martin Gansser <linux4martin@gmx.de> 1.0.4-3
- corrected scriptlets

* Mon Oct 29 2012 Martin Gansser <linux4martin@gmx.de> 1.0.4-2
- corrected URL

* Sun Oct 28 2012 Martin Gansser <linux4martin@gmx.de> 1.0.4-1
- new release
- added git revision in numbering
- corrected path in file section
- added runtime Requirement hicolor-icon-theme
- added Instructions for checking out the sources
- added %%desktop-file-validate
- shortened description

* Fri Oct 19 2012 Martin Gansser <linux4martin@gmx.de> 1.0.3-2
- added gnome-icon-theme and pywebkitgtk as requirement

* Fri Oct 19 2012 Martin Gansser <linux4martin@gmx.de> 1.0.3-1
- corrected download command for gmediafinder sources
- removed desktop patch
- changed %%desktopdir to %%datadir in file section
- added Build Requirement intltool
- rebuild for new release

* Sat Oct 13 2012 Martin Gansser <linux4martin@gmx.de> 1.0.1-1
- initial rebuild for Fedora 18
