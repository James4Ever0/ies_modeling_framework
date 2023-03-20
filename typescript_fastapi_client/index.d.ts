type RequestResult<Data> = Promise<{ response: Response; data: Data; }>;

type ReadItemsItemsGetParams0 = { "query"?: { "q"?: number; }; };
type ReadItemsItemsGetResult0 = RequestResult<object>;
/**
* summary for get items
*/
export function readItemsItemsGet(params: ReadItemsItemsGetParams0): ReadItemsItemsGetResult0;

type PostItemApiNameItemsPostParams0 = { "body"?: { "name": string; "price": number; "is_offer": boolean; "myDict": object; }; };
type PostItemApiNameItemsPostResult0 = RequestResult<{ "ans": string; "ans_1": string; }>;
/**
* summary for creating an item
* api for creating an item
*/
export function postItemApiNameItemsPost(params: PostItemApiNameItemsPostParams0): PostItemApiNameItemsPostResult0;

