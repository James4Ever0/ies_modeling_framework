import highspy

h = highspy.Highs()
filename = 'exported.mps'
h.readModel(filename)
h.run()
print('Model ', filename, ' has status ', h.getModelStatus())