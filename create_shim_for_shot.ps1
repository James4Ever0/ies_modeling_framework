# all shims are the same. they just with different names and read different .shim files.
New-Item -Path C:/Users/ss/scoop/shims/SHOT.shim -Value 'path = C:\Users\ss\Downloads\SHOT\SHOT.exe'
Copy-Item -Path C:/Users/ss/scoop/shims/pandoc.exe -Destination C:/Users/ss/scoop/shims/SHOT.exe