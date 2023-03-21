import { request } from './request';

export function readItemsItemsGet(params) {
  return request("get", `/items/`, { "header": { "Content-Type": "application/json", }, })(params);
}

export function postItemApiNameItemsPost(params) {
  return request("post", `/items/`, { "header": { "accept": "application/json", "Content-Type": "application/json", }, })(params);
}

