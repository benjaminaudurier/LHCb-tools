import imp

from Configurables import DecayTreeTuple


# __________________________________
def TestModule(module):	
	try:
		imp.find_module(module)
		found = True
	except ImportError:
		found = False

	return found


# __________________________________
def MakeDecayTreeTulple(name, location, decay_channel, TupleToolList):
	# create the tuple
	dtt = DecayTreeTuple(name)
	dtt.Inputs = [location]
	dtt.Decay = decay_channel

	# AddToople tool
	if TupleToolList is not None and len(TupleToolList) > 0:
		for TupleTool in TupleToolList:
			ok_module = TestModule(TupleTool)
			if ok_module:
				dtt.addTupleTool(TupleTool)
			else:
				print "Cannot add TupleTool {}, did you import it ?".format(TupleTool)

	return dtt


