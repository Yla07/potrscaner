# Python Portsacaner

This is a simple nmap ui for nmap port scanning. It reqires nmap installed to work.
There are two versions of the program gui and cli.

Program currently works only on window but will have linux version in the future

## GUI 
This section descripes the features of the GUI version of the app.
### Basics 
You can launch the Gui by running gui.py. To start the scan you must provide the tagrgets IP address and starting and ending ports and press run.
e.g.
 <img src = "img\readme\img1.png">

After pressing the run button the output will be displayed on the rigth side of the apps window. It will look something like this:
<img src = "img\readme\img2.png">

### OS Sacnning
To run the nmap scan with OS detection  check the "Enable OS Scan" checkbox 
e.g.
<img src="img\readme\img3.png">

### Settings
When you click the settings tab you can  change some features like location to your nmap files or the light and dark mode. You can press save to save your changes, they will be stored in data/user/user_settings.json file.

<table>
<tr>
<td>Dark Mode</td>
<td>Ligth mode</td>
</tr>
<tr>
<td>
<img src="img\readme\img4.2.png">
</td>
<td>
<img src="img\readme\img4.1.png">
</td>
</tr>
</table>

### Advanced settings 

In advanced settings you can change the backgroun dcolor of the open ports and closed ports by providing hex values.
<img src="img/readme/img5.png">

## CLI

Cli version works the same way as the gui version just without the colors and settings.

<img src= "/img/readme/img6.png">