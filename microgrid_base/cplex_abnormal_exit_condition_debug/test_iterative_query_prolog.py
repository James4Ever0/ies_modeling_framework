from swiplserver import PrologMQI

prolog_file_path = 'test_iterative_query.pro'
# query = 'member(X, [a,b,c])'
query = 'dog(X)'
with PrologMQI() as mqi:
    with mqi.create_thread() as prolog_thread:
        prolog_thread.query(f'["{prolog_file_path}"].')
        obj = prolog_thread.query_async(query, find_all=False)
        while True:
            result = prolog_thread.query_async_result()
            if result is None:
                break
            else:
                print('fetched result:', result)

# fetched result: [{'X': 'pet'}]
# fetched result: [{'X': 'animal'}]
# fetched result: [{'X': 'cute'}]