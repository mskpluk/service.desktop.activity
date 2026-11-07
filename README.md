# Desktop Activity

Kodi service add-on for Kodi running on a Linux desktop. It reports remote
control input in Kodi to the desktop as user activity.

The desktop only sees its own keyboard and mouse. When Kodi is controlled
by CEC or a phone app, the desktop thinks nobody is there: it dims the
screen and may not bring it back when you use the remote. This add-on calls
`org.freedesktop.ScreenSaver.SimulateUserActivity` when Kodi gets input (at
most every 10 seconds) and when a video starts, resumes or stops. When nothing
happens, the desktop still dims and turns off the screen as configured.

## Requirements

- Kodi 21 or newer in a desktop session that provides
  `org.freedesktop.ScreenSaver` (tested on KDE Plasma 6, Wayland)
- `gdbus` (Debian/Ubuntu: `libglib2.0-bin`)

## Install

Download `service.desktop.activity-<version>.zip` (not "Source code")
from [Releases](https://github.com/mskpluk/service.desktop.activity/releases)
and use *Add-ons → Install from zip file*. This needs *Unknown sources*
enabled in *Settings → System → Add-ons*.

## License

GPL-2.0-or-later
