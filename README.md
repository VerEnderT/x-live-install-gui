# x-live-install-gui
  [De] Erstellen Sie eine Installations-GUI für Apt und/oder Flatpak  [En] Create an installation GUI for Apt and/or Flatpak

SYNOPSIS
       x-live-install-gui [options]

OPTIONS
<br>-deb pakage
<br>define the debian pakage
    
<br>-flat Flatpak-ID
<br>define the Flatpak-ID for the programm wich will be install
    
<br>-pic image-Url
<br>define the background image in png or jpg no webp or  something like that

<br>-name program-name
<br>    defines the name of the window an in the titleline

<br>-desc description
<br>    defines the description of the programm you want to install


<h>EXAMPLES
<br>this is a example for 0 A.D.:
<br>
'''
x-live-install-gui -name '0 A.D.' -deb 0ad -flat com.play0ad.zeroad -pic 'https://play0ad.com/wp-content/gallery/screenshots/EgyptianPyramids.jpg' -desc 'a free, open-source game of ancient warfare'
'''
