# all shims are the same. they just with different names and read different .shim files.
New-Item -Path C:/Users/ss/scoop/shims/ipopt.shim -Value 'path = C:\Users\ss\Downloads\Ipopt-3.14.11-win64-msvs2019-md\bin\ipopt.exe'
Copy-Item -Path C:/Users/ss/scoop/shims/pandoc.exe -Destination C:/Users/ss/scoop/shims/ipopt.exe