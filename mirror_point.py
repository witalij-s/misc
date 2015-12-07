import numpy as np

# A paper for transforming rpy to homogenous coordinates and back, can be found here:
# http://www.diag.uniroma1.it/~deluca/rob1_en/08_EulerRPYHomogeneous.pdf
def mirrorWorkspacePoint(x, y, z, a, b, c):

	# print input
	print "#############"
	print "### INPUT ###"
	print "#############"
	print "XYZ: %d | %d | %d " % (x, y, z)
	print "ABC: %f | %f | %f " % (a, b, c)

	# Create the origin trafo with the point translation, transformation from the paper mentioned above
	point = np.matrix([[np.cos(a)*np.cos(b), np.cos(a)*np.sin(b)*np.sin(c)-np.sin(a)*np.cos(c), np.cos(a)*np.sin(b)*np.cos(c)+np.sin(a)*np.sin(c),x],
					[np.sin(a)*np.cos(b), np.sin(a)*np.sin(b)*np.sin(c)+np.cos(a)*np.cos(c), np.sin(a)*np.sin(b)*np.cos(c)-np.cos(a)*np.sin(c),y],
					[-np.sin(b), np.cos(b)*np.sin(c), np.cos(b)*np.cos(c), z],
					[0,0,0,1]])	

	# Create the homogenous mirror matrix
	mirror_xz = np.matrix([[1,0,0,0],
						[0,-1,0,0],
						[0,0,1,0],
						[0,0,0,1]])

	# result of transformation
	result = mirror_xz * point

	# Print the point which will be transformated
	print("\nPoint")
	print("------")
	print(np.round(point))
	print("")

	# The orientation RPY / ABC variables
	alpha = beta = gamma = 0

	# Calculate ABC from homogenous matrix
	if (result[0,0] == result [1,0] and result [0,0] == 0.):
		print "Debug: Case 1"
		alpha = 0
		beta = np.pi/2.
		gamma = np.arctan2(result[0,1], result[1,1])
	else:
		print "Debug: Case 2"
		beta = np.arctan2(-result[2,0], np.sqrt(np.square(result[2,1])+np.square(result[2,2])))	
		alpha = np.arctan2(result[1,0]/np.cos(beta), result[0,0]/np.cos(beta))
		#gamma = np.arctan2(result[2,1], result[2,2])
		gamma = np.arctan2(result[2,1]/np.cos(beta), result[2,2]/np.cos(beta))

	####### HACK I DONT KNOW WHY #######
	gamma = -gamma

	# print XYZ ABC representation
	print "\n##############"
	print "### OUTPUT ###"
	print "##############"
	print "XYZ: %d | %d | %d " % (result[0,3], result[1,3], result[2,3])
	print "ABC: %f | %f | %f " % (alpha, beta, gamma);

	# command for telnet
	print "\nTelnet command"
	print "----------------"
	print "(Start) ptp move : %d %d %d %f %f %f 0.2 0.0" % (x, y, z, a, b, c)
	print "(Final) ptp move : %d %d %d %f %f %f 0.2 0.0" % (result[0,3], result[1,3], result[2,3], alpha, beta, gamma)

####################
####  Example  #####
####################

# Costume point 
mirrorWorkspacePoint(-63.4709539762285, -297.90564707226673, 1096.71747634639, -2.3434756027019388, 0.8819053837303993, -0.2372932845653568)