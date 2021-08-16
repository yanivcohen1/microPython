# use: .\connect.ps1 comNumber  
# .\connect.ps1 6 # esp32 no spram
# .\connect.ps1 7 # esp32 spram
$port_name=$args[0]
venv\Scripts\activate
rshell --editor nano --buffer-size=30 -p COM$port_name