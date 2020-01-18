%global gtk3_version    %(pkg-config --modversion gtk+-3.0 2>/dev/null || echo bad)
%global glib2_version   %(pkg-config --modversion glib-2.0 2>/dev/null || echo bad)
%global nm_version      1:1.1.0
%global obsoletes_ver   1:0.9.7

%global rpm_version 1.8.0
%global real_version 1.8.0
%global release_version 3

Name: network-manager-applet
Summary: A network control and status applet for NetworkManager
Version: %{rpm_version}
Release: %{release_version}%{?dist}
Group: Applications/System
License: GPLv2+
URL: http://www.gnome.org/projects/NetworkManager/
Obsoletes: NetworkManager-gnome < %{obsoletes_ver}

Source: https://download.gnome.org/sources/network-manager-applet/1.8/%{name}-%{real_version}.tar.xz
Patch0: nm-applet-no-notifications.patch
Patch1: 0001-translations-rh1379642.patch
Patch2: 0002-editor-fix-8021x-crash-rh1458567.patch

Requires: NetworkManager >= %{nm_version}
Requires: NetworkManager-glib >= %{nm_version}
Requires: libnma%{?_isa} = %{version}-%{release}
Requires: libnotify >= 0.4.3
Requires: gnome-icon-theme
Requires: nm-connection-editor = %{version}-%{release}

BuildRequires: NetworkManager-devel >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: NetworkManager-libnm-devel >= %{nm_version}
BuildRequires: ModemManager-glib-devel >= 1.0
BuildRequires: glib2-devel >= 2.32
BuildRequires: gtk3-devel >= 3.10
BuildRequires: libsecret-devel
BuildRequires: gobject-introspection-devel >= 0.10.3
BuildRequires: gettext-devel
BuildRequires: /usr/bin/autopoint
BuildRequires: pkgconfig
BuildRequires: libnotify-devel >= 0.4
BuildRequires: automake autoconf intltool libtool
BuildRequires: gtk-doc
BuildRequires: desktop-file-utils
BuildRequires: iso-codes-devel
BuildRequires: libgudev1-devel >= 147
BuildRequires: libsecret-devel >= 0.12
BuildRequires: jansson-devel
BuildRequires: gcr-devel
BuildRequires: libselinux-devel

%description
This package contains a network control and status notification area applet
for use with NetworkManager.

%package -n nm-connection-editor
Summary: A network connection configuration editor for NetworkManager
Requires: NetworkManager-glib >= %{nm_version}
Requires: libnma%{?_isa} = %{version}-%{release}
Requires: gnome-icon-theme
Requires(post): /usr/bin/gtk-update-icon-cache

%description -n nm-connection-editor
This package contains a network configuration editor and Bluetooth modem
utility for use with NetworkManager.


%package -n libnm-gtk
Summary: Private libraries for NetworkManager GUI support
Group: Development/Libraries
Requires: gtk3 >= %{gtk3_version}
Requires: mobile-broadband-provider-info >= 0.20090602
Obsoletes: NetworkManager-gtk < %{obsoletes_ver}

%description -n libnm-gtk
This package contains private libraries to be used only by nm-applet,
nm-connection editor, and the GNOME Control Center.

%package -n libnm-gtk-devel
Summary: Private header files for NetworkManager GUI support
Group: Development/Libraries
Requires: NetworkManager-devel >= %{nm_version}
Requires: NetworkManager-glib-devel >= %{nm_version}
Obsoletes: NetworkManager-gtk-devel < %{obsoletes_ver}
Requires: libnm-gtk = %{version}-%{release}
Requires: gtk3-devel
Requires: pkgconfig

%description -n libnm-gtk-devel
This package contains private header and pkg-config files to be used only by
GNOME control center.

This package is obsoleted by libnma.


%package -n libnma
Summary: Private libraries for NetworkManager GUI support
Group: Development/Libraries
Requires: gtk3 >= %{gtk3_version}
Requires: mobile-broadband-provider-info >= 0.20090602
Obsoletes: NetworkManager-gtk < %{obsoletes_ver}

%description -n libnma
This package contains private libraries to be used only by nm-applet,
nm-connection editor, and the GNOME Control Center.

%package -n libnma-devel
Summary: Private header files for NetworkManager GUI support
Group: Development/Libraries
Requires: NetworkManager-devel >= %{nm_version}
Requires: NetworkManager-libnm-devel >= %{nm_version}
Obsoletes: NetworkManager-gtk-devel < %{obsoletes_ver}
Requires: libnma = %{version}-%{release}
Requires: gtk3-devel
Requires: pkgconfig

%description -n libnma-devel
This package contains private header and pkg-config files to be used only by
nm-applet, nm-connection-editor, and the GNOME control center.

This package deprecates libnm-gtk.

%prep
%setup -q -n "%{name}-%{real_version}"
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoreconf -i -f
intltoolize --force
%configure \
    --with-gcr \
    --with-selinux \
    --disable-static \
    --enable-more-warnings=yes
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%find_lang nm-applet
cat nm-applet.lang >> %{name}.lang

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# validate .desktop and autostart files
desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nm-applet.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/nm-connection-editor.desktop


%post	-n libnma -p /sbin/ldconfig
%postun	-n libnma -p /sbin/ldconfig

%post	-n libnm-gtk -p /sbin/ldconfig
%postun	-n libnm-gtk -p /sbin/ldconfig

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post -n nm-connection-editor
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%postun -n nm-connection-editor
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%posttrans -n nm-connection-editor
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files
%{_bindir}/nm-applet
%{_datadir}/applications/nm-applet.desktop
%{_datadir}/icons/hicolor/22x22/apps/nm-adhoc.png
%{_datadir}/icons/hicolor/22x22/apps/nm-mb-roam.png
%{_datadir}/icons/hicolor/22x22/apps/nm-secure-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-signal-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-stage*-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-tech-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-active-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-wwan-tower.png
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_mandir}/man1/nm-applet*
%doc NEWS AUTHORS README CONTRIBUTING
%license COPYING

# Yes, lang files for the applet go in nm-connection-editor RPM since it
# is the RPM that everything else depends on
%files -n nm-connection-editor -f %{name}.lang
%{_bindir}/nm-connection-editor
%{_datadir}/applications/nm-connection-editor.desktop
%{_datadir}/icons/hicolor/*/apps/nm-device-*.*
%{_datadir}/icons/hicolor/*/apps/nm-no-connection.*
%{_datadir}/icons/hicolor/16x16/apps/nm-vpn-standalone-lock.png
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%{_datadir}/appdata/nm-connection-editor.appdata.xml
%{_mandir}/man1/nm-connection-editor*
%dir %{_datadir}/gnome-vpn-properties

%files -n libnm-gtk
%{_libdir}/libnm-gtk.so.*
%{_libdir}/girepository-1.0/NMGtk-1.0.typelib

%files -n libnm-gtk-devel
%dir %{_includedir}/libnm-gtk
%{_includedir}/libnm-gtk/*.h
%{_libdir}/pkgconfig/libnm-gtk.pc
%{_libdir}/libnm-gtk.so
%{_datadir}/gir-1.0/NMGtk-1.0.gir

%files -n libnma
%{_libdir}/libnma.so.*
%{_libdir}/girepository-1.0/NMA-1.0.typelib

%files -n libnma-devel
%dir %{_includedir}/libnma
%{_includedir}/libnma/*.h
%{_libdir}/pkgconfig/libnma.pc
%{_libdir}/libnma.so
%{_datadir}/gir-1.0/NMA-1.0.gir
%{_datadir}/gtk-doc


%changelog
* Tue Jun  6 2017 Beniamino Galvani <bgalvani@redhat.com> - 1.8.0-3
- editor: fix crash when destroying 802.1x page (rh #1458567)

* Mon May 29 2017 Lubomir Rintel <lrintel@redhat.com> - 1.8.0-2
- po: update Japanese translation (rh #1379642)

* Wed May 10 2017 Thomas Haller <thaller@redhat.com> - 1.8.0-1
- Update to 1.8.0 release (rh #1441621)

* Tue Mar 28 2017 Lubomir Rintel <lrintel@redhat.com> - 1.8.0-0.1.git20170326.f260f8a
- Update to network-manager-applet 1.8 snapshot
- c-e: add missing mnemonic characters to buttons (rh #1434317)
- c-e: fix handling of devices without permanent MAC address in devices combo box (rh #1380424)

* Thu Sep 22 2016 Lubomir Rintel <lrintel@redhat.com> - 1.4.0-2
- c-e: fix team page with older GTK and jansson (rh #1079465)

* Wed Aug 24 2016 Lubomir Rintel <lrintel@redhat.com> - 1.4.0-1
- Update to network-manager-applet 1.4.0 release
- c-e: add editor for teaming devices (rh #1079465)

* Sat Aug 20 2016 Thomas Haller <thaller@redhat.com> - 1.2.2-2
- c-e: fix tab stop for Create button (rh#1339565)

* Fri Jul 08 2016 Lubomir Rintel <lrintel@redhat.com> - 1.2.2-1
- Update to network-manager-applet 1.2.2 release

* Wed Apr 27 2016 Lubomir Rintel <lrintel@redhat.com> - 1.2.0-1
- Update to network-manager-applet 1.2.0 release

* Wed Mar 30 2016 Lubomir Rintel <lrintel@redhat.com> - 1.2.0-0.1.beta3
- Rebase to 1.2-beta3

* Wed Sep 30 2015 Jiří Klimeš <jklimes@redhat.com> - 1.0.6-2
- libnm-gtk: fix a possible crash on widgets destroy (rh #1267326)
- libnm-gtk: use symbolic icons for password store menu (rh #1267330)

* Tue Jul 14 2015 Lubomir Rintel <lrintel@redhat.com> - 1.0.6-1
- Align with the 1.0.6 upstream release:
- editor: add support for setting MTU on team connections (rh #1255927)
- editor: offer bond connections in vlan slave picker (rh #1255735)

* Tue Jul 14 2015 Lubomir Rintel <lrintel@redhat.com> - 1.0.4-1
- Align with the upstream release

* Wed Jun 17 2015 Jiří Klimeš <jklimes@redhat.com> - 1.0.3-2.git20150617.a0b0166
- New snapshot:
- editor: let users edit connection.interface-name property (rh #1139536)

* Mon Jun 15 2015 Lubomir Rintel <lrintel@redhat.com> - 1.0.3-1.git20160615.28a0e28
- New snapshot:
- applet: make new auto connections only available for current user (rh #1176042)
- editor: allow forcing always-on-top windows for installer (rh #1097883)
- editor: allow changing bond MTU (rh #1177582)
- editor: use ifname instead of UUID in slaves' master property (rh #1083186)
- editor: allow adding Bluetooth connections (rh #1229471)

* Tue May 19 2015 Debarshi Ray <rishi@fedoraproject.org> - 1.0.0-3.git20150122.76569a46
- Drop gnome-bluetooth BR because it does not work with newer versions (rh #1174547)

* Thu Jan 22 2015 Dan Williams <dcbw@redhat.com> - 1.0.0-2.git20150122.76569a46
- editor: fix IPoIB editing support (rh #1182560)

* Fri Jan  9 2015 Dan Williams <dcbw@redhat.com> - 1.0.0-1
- Update to 1.0 release

* Tue Nov 25 2014 Dan Williams <dcbw@redhat.com> - 0.9.11.0-2.git20141125.b4973b85
- New snapshot

* Wed Nov 19 2014 Dan Williams <dcbw@redhat.com> - 0.9.11.0-1.git20141119.a06c7cd3
- Update translations (rh #1081943)
- Allow creating master devices without slaves (rh #1075198)

* Wed Mar 26 2014 Dan Winship <danw@redhat.com> - 0.9.9.0-15.git20140307
- Make Bluetooth plugin work more than once (rh #1054212)

* Thu Mar 20 2014 Dan Winship <danw@redhat.com> - 0.9.9.0-14.git20140307
- Add ModemManager-glib-devel to BuildRequires to fix Bluetooth (rh #1054212)

* Fri Mar  7 2014 Jiří Klimeš <jklimes@redhat.com> - 0.9.9.0-13.git20140307
- Update to new git master snapshot
- connection-editor: allow VLANs/slaves of more device types (rh #1045203)
- connection-editor: add DCB configuration UI (bgo #711032) (rh #1068688) 

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.9.9.0-12.git20131212
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Dan Winship <danw@redhat.com> - 0.9.9.0-11.git20131212
- Fix keyboard activation of bridge priority field (rh #1036142)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.9.9.0-10.git20131212
- Mass rebuild 2013-12-27

* Fri Dec 13 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-9.git20131212
- applet: fix crash if some resources were not available (rh #1034500)
- editor: default to user-saved secrets and allow changing secret storage (rh #879566)
- applet/editor: fix various Coverity-found defects (rh #1025894)

* Fri Nov  8 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-8.git20131108
- editor: improve handling of NPAR/SRIOV devices in bonds (rh #804527)
- editor: allow creating bridge masters without slaves

* Fri Oct 11 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-7.git20131011
- editor: add support for Team devices (rh #1003646)
- editor: don't use deprecated WEP40 and WEP104 values for pairwise (rh #1005171)
- editor: add 'primary' option for bond interfaces (rh #1013727)
- editor: dis-allow IPv6 scopes in DNS server entry (rh #962449)

* Fri Sep 13 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-6.git20130906
- libnm-gtk: fix for enabling the Apply button for PEAP and TTLS (rh #1000564)
- libnm-gtk: only save CA certificate ignored value when connection is saved
- editor: fix display of VLAN parent interface

* Fri Sep 06 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-5.git20130906
- editor: fix missing user/password when re-editing a connection (rh #1000564)
- editor: fix handling of missing CA certificate prompts (rh #758076) (rh #809489)
- editor: fix handling of bonding modes (rh #953076)
- applet/editor: add InfiniBand device support (rh #867273)

* Tue Aug 06 2013 Dennis Gilmore <dennis@ausil.us> - 0.9.9.0-4.git20130515
- rebuild for soname bump in gnome-bluetooth

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.0-3.git20130515
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-2
- Disable migration tool and remove dependencies on GConf and gnome-keyring

* Wed May 15 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-1.git20130515
- Update to 0.9.10 snapshot

* Tue Apr 30 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-3.git20130430
- editor: fix possible crash canceling connection edit dialog
- applet: only request secrets from the user when allowed to
- applet: fix signal icons with newer libpng
- applet: fix possible crash getting secrets with libsecret

* Thu Apr 18 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.8.1-2.git20130327
- applet: fix crash while getting a PIN to unlock a modem (rh #950925)

* Wed Mar 27 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-1.git20130327
- Update to 0.9.8.2 snapshot
- Updated translations
- editor: don't overwrite bridge/bond master interface name with UUID
- applet: fix WWAN PIN dialog invalid "label1" entry widget
- editor: fix allowed values for VLAN ID and MTU
- editor: preserve existing PPP connection LCP echo failure and reply values
- editor: ensure changes to the STP checkbox are saved
- editor: hide BSSID for AdHoc connection (rh #906133)
- editor: fix random data sneaking into IPv6 route gateway fields
- editor: fix handling of initial entry for MAC address widgets

* Wed Feb 27 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.8.0-1
- Update to 0.9.8.0

* Fri Feb  8 2013 Dan Williams <dcbw@redhat.com> - 0.9.7.997-1
- Update to 0.9.7.997 (0.9.8-beta2)
- editor: better handling of gateway entry for IPv4
- editor: fix some mnemonics (rh #893466)
- editor: fix saving connection when ignoring CA certificate
- editor: enable Bridge connection editing
- editor: hide widgets not relevant for VPN connections

* Tue Dec 11 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-6.git20121211
- editor: fix populating Firewall zone in 'General' tab

* Tue Dec 11 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-5.git20121211
- Update to git snapshot (git20121211) without bridges

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.7.0-4.git20121016
- Update the versioned obsoletes for the new F17 NM build

* Tue Oct 16 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-3.git20121016
- Update to git snapshot (git20121016)
- editor: fix a crash when no VPN plugins are installed

* Thu Oct  4 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-3.git20121004
- Update to git snapshot

* Wed Sep 12 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-3.git20120820
- move GSettings schema XML to nm-connection-editor rpm (rh #852792)

* Thu Aug 30 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-2.git20120820
- run glib-compile-schemas in %post scriplet (rh #852792)

* Tue Aug 21 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-1.git20120820
- Update to 0.9.7.0 snapshot

* Tue Aug 14 2012 Daniel Drake <dsd@laptop.org> - 0.9.5.96-2
- Rebuild for libgnome-bluetooth.so.11

* Mon Jul 23 2012 Dan Williams <dcbw@redhat.com> - 0.9.5.96-1
- Update to 0.9.6-rc2
- lib: recognize PKCS#12 files exported from Firefox
- lib: fix some wireless dialog crashes

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.95-3.git20120713
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.5.95-2.git20120713
- Fix the versioned obsoletes

* Fri Jul 13 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.5.95-1.git20120713
- update to 0.9.5.95 (0.9.6-rc1)  snapshot
- editor: fixed UI mnemonics
- editor: fix defaults for PPP echo values
- applet: various crash and stability fixes
- applet: show IPv6 addressing page for VPN plugins that support it
- applet: port to GSettings and split out 0.8 -> 0.9 migration code into standalone tool

* Mon May 21 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-4
- update to git snapshot

* Wed May  2 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-3
- update to git snapshot

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.997-1
- Initial package split from NetworkManager

