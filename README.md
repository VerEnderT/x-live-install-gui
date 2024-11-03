# x-live-install-gui
  [De] Erstellen Sie eine Installations-GUI für Apt und/oder Flatpak  [En] Create an installation GUI for Apt and/or Flatpak

SYNOPSIS
       x-live-install-gui [options]

OPTIONS
-deb pakage
define the debian pakage
    
-flat Flatpak-ID
define the Flatpak-ID for the programm wich will be install
    
-pic image-Url
define the background image in png or jpg no webp or  something like that

-name program-name
    defines the name of the window an in the titleline

-desc description
    defines the description of the programm you want to install


EXAMPLES
       this is a example for 0 A.D.:
'''x-live-install-gui -name '0 A.D.' -deb 0ad -flat com.play0ad.zeroad -pic 'https://play0ad.com/wp-content/gallery/screenshots/EgyptianPyramids.jpg' -desc 'a free, open-source game of ancient warfare'
'''



              defines the description of the programm you want to install
'''
