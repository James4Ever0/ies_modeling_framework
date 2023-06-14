import ninja.ninja_syntax as NS

output_path = "test.ninja"
with open(output_path, 'w+') as f:
    wt = NS.Writer(f)
    wt.comment('comment text')
    # wt.close()