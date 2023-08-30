@REM D:
@REM cd D:\project\xianxing
@REM date /T
@REM time /T
@REM git pull
@REM git add .
@REM git commit -m 'update'
@REM git push
@REM install gptcommit: cargo install --locked gptcommit

echo %USERNAME% executed commit script at %DATE% %TIME%
git config --global --add safe.directory E:/works/jubilant-adventure3
git pull origin_devops main
git add .
git commit --no-edit
@REM git commit -m 'update'
git push origin_devops main
git push origin main


cd microgrid_base/dsl_parser
git config --global --add safe.directory E:/works/jubilant-adventure3/microgrid_base/dsl_parser
git pull origin_devops main
git add .
@REM git commit -m 'update'
git commit --no-edit
git push origin_devops main
git push origin main
cd ../..
