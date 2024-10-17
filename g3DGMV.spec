%define name	g3DGMV
%define version	0.60
%define release %mkrel 6

Name: 	 	%{name}
Summary: 	3D digital map viewer for GNOME
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
Source1: 	%{name}48.png
Source2: 	%{name}32.png
Source3: 	%{name}16.png
# (fc) 0.60-2mdk fix build
Patch0:		g3DGMV-0.60-fixbuild.patch.bz2

URL:		https://g3dgmv.sourceforge.net/
License:	GPL
Group:		Sciences/Geosciences
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gettext gnome-libs-devel

%description
The g3DGMV program was designed as a free viewer for Digital Elevation Model
(DEM ) and Digital Line Graphs (DLG ) maps. Both of these formats are available
from various locations on the web. These maps are rendered by g3DGMV as 3D
images that can be manipulated by the user and view from different angles.

In addition g3DGMV can read maps that have been saved as bitmaps (gif ,png,
jpeg ,xpm). Because these formats do not contain elevation information they
are viewable only in 2D mode.

The program contains many utilitys that enable the user to add his/her own
location information to these maps. These tools can be used to mark a favorite
camp site or highlight the best route to some location.

%prep
%setup -q
%patch0 -p1 -b .fixbuild

%build
%configure
# de locale is broken as of v0.60
perl -p -i -e 's/de.po\ //g' `find -name Makefile`
perl -p -i -e 's/de.gmo\ //g' `find -name Makefile`
rm -f po/de.po po/de.gmo
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

#menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%name.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Icon=%{name}
Name=g3DGMV
Comment=3D Map Viewer
Categories=Education;Science;Geology;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
cat %SOURCE1 > $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
cat %SOURCE2 > $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
cat %SOURCE3 > $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif
		
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README ChangeLog AUTHORS COPYING NEWS
%{_bindir}/%name
%{_datadir}/applications/mandriva-%name.desktop
%{_datadir}/gnome/help/gnome-%name
%{_datadir}/gnome/apps/Applications/*.desktop
%{_datadir}/pixmaps/*.png
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

