# all shims are the same. they just with different names and read different .shim files.
New-Item -Path C:/Users/ss/scoop/shims/node.shim -Value 'path = C:\ProgramData\scoop\apps\nodejs\19.7.0\node.exe'
Copy-Item -Path C:/Users/ss/scoop/shims/pandoc.exe -Destination C:/Users/ss/scoop/shims/node.exe