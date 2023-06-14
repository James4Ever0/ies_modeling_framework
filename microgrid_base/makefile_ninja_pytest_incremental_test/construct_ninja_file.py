import ninja.ninja_syntax as NS

output_path = "test.ninja"
wt = NS.Writer(output_path)

wt.comment('comment text')
# wt.close()