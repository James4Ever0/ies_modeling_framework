port = 3398
MAX_TASK_COUNT=3
TEST_GRAPH_CONFIG

class endpoint_suffix:
    UPLOAD_GRAPH_ASYNC: str = "upload_graph_async"
    UPLOAD_GRAPH: str = "upload_graph"
    CHECK_RESULT_ASYNC: str = "check_result_async"

url_base = f"http://localhost:{port}"

get_url = lambda suffix: f"{url_base}/{suffix}"

# will refuse connection if current task count is above 3.

upload_url = get_url(endpoint_suffix.UPLOAD_GRAPH)

async_url = get_url(endpoint_suffix.UPLOAD_GRAPH_ASYNC)
check_result_async = get_url(endpoint_suffix.CHECK_RESULT_ASYNC)
