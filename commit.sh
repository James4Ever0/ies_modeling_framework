git pull
git add .
git commit -m 'update'
git push origin_devops main
env http_proxy="" https_proxy="" git push origin main
# TODO: let chatgpt-like bots generate this commit message.

cd microgrid/dsl_parser
git pull
git add .
git commit -m 'update'
git push origin_devops main
env http_proxy="" https_proxy="" git push origin main
