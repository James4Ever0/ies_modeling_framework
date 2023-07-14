@REM D:
@REM cd D:\project\xianxing
@REM date /T
@REM time /T
@REM git pull
@REM git add .
@REM git commit -m 'update'
@REM git push
echo %USERNAME% executed commit script at %DATE% %TIME%
git config --global --add safe.directory E:/works/jubilant-adventure2
git pull
git add .
git commit -m 'update'
git push origin_devops main
git push origin main



cd microgrid/dsl_parser
git pull
git add .
git commit -m 'update'
git push origin_devops main
git push origin main
cd ../..
