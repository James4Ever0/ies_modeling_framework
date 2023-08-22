git pull origin_devops main
git add .
git commit --no-edit
#git commit -m 'update'
git push origin_devops main
env http_proxy="" https_proxy="" git push origin main
# TODO: let chatgpt-like bots generate this commit message.

cd microgrid_base/dsl_parser
git pull origin_devops main
# shall you filter anything too big under this folder before commit, add them to .gitignore
git add .
git commit --no-edit
#git commit -m 'update'
git push origin_devops main
env http_proxy="" https_proxy="" git push origin main
