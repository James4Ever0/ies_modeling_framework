port = 3398

url_base= f"http://localhost:{port}"

get_url = lambda suffix: f"{url_base}/{suffix}"

# will refuse connection if current task count is above 3.

upload_url = get_url("upload_graph")

async_url = get_url("upload_graph_async")
check_result_async = get_url("check_result_async")