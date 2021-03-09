#!/bin/bash

BASE_DIR=$(cd $(dirname $0); pwd)

GIT_BRANCH="webhook_v2.5-jiaxing"
GIT_USER_NAME="coding@coding.com"
GIT_CODE_URL="http://e.szv3.devops.jx/codingcorp/jiaxingyinhang/coding-frontend.git"
GIT_USER_PASSWD="coding123"
CODING_REGISTRY_USER="release-1615789307724"
CODING_REGISTRY_PASS="7c7b092355b40f55324e99d861da2c281f8096c7"
UPLOAD_STATIC_RESOURCES_TO_CDN="false"
CODING_REGISTRY_URL="codingcorp-docker.pkg.szv3.devops.jx"
CODING_PROJECT="jiaxingyinhang"
CODING_REGISTRY_REPO="${CODING_PROJECT}/release"
# BASE_IMAGE="codingcorp-docker.pkg.szv3.devops.jx/jiaxingyinhang/public/centos-yarn:latest"
BASE_IMAGE="node-yarn"


function get_latest_code(){
  CODE_REPO=${GIT_CODE_URL##*/}
  CODE_REPO=${CODE_REPO%%.*}
  CODE_PATH=${BASE_DIR}/workspase/${CODE_REPO}
  check_git_info
  echo "Get the latest code for $CODE_REPO"
  [[ ! -d "$BASE_DIR/workspase/" ]] && mkdir -p $BASE_DIR/workspase/
  if [[ ! -d $CODE_PATH ]];then
    cd $(dirname $CODE_PATH)
    git clone -b $GIT_BRANCH $GIT_CODE_URL
  fi
  cd ${CODE_PATH}; git checkout $GIT_BRANCH
}


function check_git_info(){
  echo "Check the git repo information"
  if [ -f "~/.gitconfig" -a `cat  ~/.gitconfig| grep $GIT_USER_NAME | wc -l` -lt 0 ];then
    echo "git info ..."
  else
    git config --global user.email $GIT_USER_NAME
    git config --global user.password $GIT_USER_PASSWD
    git config --global credential.helper store
  fi
}


function compire_software(){

  APP_NAME=$1
  images_version=$2
  local base_image=$BASE_IMAGE:$images_version
  docker run --rm --user=root --network=host \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /usr/bin/docker:/usr/bin/docker \
    -v ${BASE_DIR}/workspase/coding-frontend:/data/ \
    -e DOCKER_HOST="unix:///var/run/docker.sock" \
    -e NPM_CONFIG_LOGLEVEL=http \
    -e SENTRY_DSN=${sentry_dsn} \
    -e PUBLIC_PATH=${PUBLIC_PATH} \
    -e STATIC_DIR=build/${app_name} \
    -e APP=${APP_NAME} \
    -e UPLOAD_STATIC_RESOURCES_TO_CDN=${UPLOAD_STATIC_RESOURCES_TO_CDN} \
    -e CODING_REGISTRY_URL=${CODING_REGISTRY_URL} \
    -e CODING_REGISTRY_REPO=${CODING_REGISTRY_REPO} \
    -e CODING_REGISTRY_USER=${CODING_REGISTRY_USER} \
    -e CODING_REGISTRY_PASS=${CODING_REGISTRY_PASS} \
    -w /data ${base_image} bash -x build.sh ${APP_NAME} --push
}


# ==================================== main ==================================
# get latset code from git
get_latest_code

case $1 in 
    enterprise-front|artifacts-admin)
      compire_software $1 "8.11.3-centos"
    ;;
    e-admin)
      compire_software $1 "6.9.1-centos"
    ;;
    *)
      if [ -z $1 ];then
        echo "USAGW: $0 <module>"
      else
        echo "Unknow module: $1"
        exit 1
      fi
      exit 0
esac
