#!/usr/bin/python3

#######################################################################
# LICENSE: 0BSD, "BSD Zero Clause License"
#
# Copyright (C) 2022, ZincLinux Team <zinc.linux.2020@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
# PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
#######################################################################
# ABOUT:
#
# Designed for ZincLinux (Debian + XFCE) @ https://zinclinux.tech.blog
# close Emacs, Geany before changing modes so their configs are updated
# Changes wallpaper if same files are in light and dark subfolder
# Configure theme, icons etc @ line # 51

import os, os.path

def xrandrActiveMonitors(prefix=''):
	xr = os.popen("xrandr --listactivemonitors").read().splitlines()[1:]
	displays = []
	for display in xr:
		displayName = display.split()[3]
		if len(prefix):
			displayName = prefix + displayName
		displays.append(displayName)
	return displays

def xfdesktopLastImageProperties(activeMonitors=[]):
	lastImageProperties = []
	for am in activeMonitors:
		qStr = 'xfconf-query -c xfce4-desktop -p /backdrop/screen0/' + am + ' -l'
		xfQuery = os.popen(qStr).read().splitlines()
		for ln in xfQuery:
			if '/last-image' in ln:
				lastImageProperties.append(ln)
	return lastImageProperties

# DARK MODE    =  (   OFF     ,      ON       )
StyleThemeName = ('Adwaita', 'Adwaita-dark')
IconThemeName = ('Papirus-Light', 'Papirus-Dark')
GeanyColorScheme = ('github.conf', 'inkpot.conf') # geany's Default is ''
WallpaperSubfolder = ('/light/','/dark/')
#KvantumTheme = ('KvArc', 'KvArcDark') # not used

# get/set dark mode file
darkMode = True
os.chdir(os.environ['HOME'] + '/.zinclinux/nightday/')
if os.path.exists('../darkmode.on'):
	os.rename('../darkmode.on', '../darkmode.off')
	darkMode = False
elif os.path.exists('../darkmode.off'):
	os.rename('../darkmode.off', '../darkmode.on')
else:
	os.mknod('../darkmode.on')

# os.system("kvantummanager --set " + KvantumTheme[darkMode]) # not used
os.system("xfconf-query -c xsettings -p /Net/ThemeName -s " + StyleThemeName[darkMode])
os.system("xfconf-query -c xsettings -p /Net/IconThemeName -s " + IconThemeName[darkMode])
os.system('sed -i "/color_scheme=/c color_scheme=' + GeanyColorScheme[darkMode] + '" ~/.config/geany/geany.conf')

# xfce4 active wallpapers
properties = xfdesktopLastImageProperties(xrandrActiveMonitors('monitor'))
for prop in properties:
	qStr = 'xfconf-query -c xfce4-desktop -p ' + prop + ' -v'
	currImg = os.popen(qStr).read().strip()
	if (WallpaperSubfolder[0] in currImg) or (WallpaperSubfolder[1] in currImg):
		newImg = currImg.replace(WallpaperSubfolder[int(not darkMode)], WallpaperSubfolder[int(darkMode)])
		if os.path.exists(newImg):
			cStr = 'xfconf-query -c xfce4-desktop -p ' + prop + ' -s "' + newImg + '"'
			os.system(cStr)
