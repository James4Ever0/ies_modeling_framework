# all shims are the same. they just with different names and read different .shim files.
New-Item -Path C:/Users/ss/scoop/shims/node.shim -Value 'path = C:\ProgramData\scoop\apps\nodejs\19.7.0\node.exe'
Copy-Item -Path C:/Users/ss/scoop/shims/pandoc.exe -Destination C:/Users/ss/scoop/shims/node.exe

New-Item -Path C:/Users/ss/scoop/shims/npm.shim -Value 'path = C:\ProgramData\scoop\apps\nodejs\19.7.0\npm.cmd'
Copy-Item -Path C:/Users/ss/scoop/shims/pandoc.exe -Destination C:/Users/ss/scoop/shims/npm.exe


New-Item -Path C:/Users/ss/scoop/shims/tsc.shim -Value 'path = C:\ProgramData\scoop\apps\nodejs\19.7.0\bin\tsc.cmd'
Copy-Item -Path C:/Users/ss/scoop/shims/pandoc.exe -Destination C:/Users/ss/scoop/shims/tsc.exe


New-Item -Path C:/Users/ss/scoop/shims/npx.shim -Value 'path = C:\ProgramData\scoop\apps\nodejs\19.7.0\npx.cmd'
Copy-Item -Path C:/Users/ss/scoop/shims/pandoc.exe -Destination C:/Users/ss/scoop/shims/npx.cmd