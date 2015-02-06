# Spec is based on Andrea Musuruane's work in Fedora

Name:		tecnoballz
Version:	0.92
Release:	2
Summary:	A Brick Busting game
Group:		Games/Arcade
License:	GPLv3+
URL:		http://linux.tlk.fr/games/TecnoballZ/
Source0:	http://linux.tlk.fr/games/TecnoballZ/download/%{name}-%{version}.tgz
Source1:	%{name}.xpm
Source2:	%{name}.desktop
# Andrea Musuruane
# Fix dependencies
Patch0:		tecnoballz-0.92-dependecies.patch
# Andrea Musuruane
# Don't combine explicit and implicit rules for make 3.82
# Set correct gamedir for Fedora
Patch1:		tecnoballz-0.92-Makefile.patch
# Debian
# Fix configure.ac Makefile.am to include missing files
Patch2:		tecnoballz-0.92-level_data.patch
Patch3:		tecnoballz-0.92-texts_dir.patch
# Debian
# Use tinyxml system library
Patch4:		tecnoballz-0.92-tinyxml.patch
# Upstream CVS
# Compile with gcc 4.3
Patch5:		tecnoballz-0.92-gcc43.patch
# Hans de Goede
# Drop setgid privileges when not needed
Patch6:		tecnoballz-0.92-dropsgid.patch

BuildRequires:	autoconf
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	libmikmod-devel
BuildRequires:	tinyxml-devel

%description
A exciting Brick Breaker with 50 levels of game and 11 special levels, 
distributed on the 2 modes of game to give the player a sophisticated 
system of attack weapons with an enormous power of fire that can be 
build by gaining bonuses. Numerous decors, musics and sounds 
complete this great game. This game was ported from the Commodore Amiga.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
# Patch4 must be called after Patch0
# It requires tinyxml >= 2.6
%if %{mdvver} >= 201100
%patch4 -p1
%endif
%patch5 -p2
%patch6 -p1


%build
autoreconf -fvi
%configure2_5x
# FIX: ovverride CXXFLAGS to pick up RPM_OPT_FLAGS
%make CXXFLAGS="%{optflags}"

%install
%__rm -rf %{buildroot}
%makeinstall_std

# install desktop file
%__mkdir_p %{buildroot}%{_datadir}/applications
%__cp %{SOURCE2} %{buildroot}%{_datadir}/applications/

# install icon
%__mkdir_p %{buildroot}%{_iconsdir}/hicolor/32x32/apps
%__install -p -m 0644 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.xpm

%clean
%__rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%doc AUTHORS CHANGES COPYING README
%attr(2755,root,games) %{_bindir}/%{name}
%{_datadir}/%{name}
%dir %{_localstatedir}/games/%{name}
%attr(-,root,games) %config(noreplace) %{_localstatedir}/games/%{name}/%{name}.hi
%{_mandir}/man6/%{name}.6*
%{_iconsdir}/hicolor/32x32/apps/%{name}.xpm
%{_datadir}/applications/%{name}.desktop



%changelog
* Tue Mar 20 2012 Andrey Bondrov <abondrov@mandriva.org> 0.92-1mdv2011.0
+ Revision: 785863
- imported package tecnoballz

