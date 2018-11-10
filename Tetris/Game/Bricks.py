
S_SHAPE_TEMPLATE =([[2,2,0],
					[0,2,2]],
				   [[0,2],
					[2,2],
					[2,0]])

Z_SHAPE_TEMPLATE =([[0,6,6],
					[6,6,0]],
				   [[6,0],
					[6,6],
					[0,6]])

I_SHAPE_TEMPLATE =([[0,0,0,0],
					[4,4,4,4],
					[0,0,0,0]],
				   [[0,4,0],
					[0,4,0],
					[0,4,0],
					[0,4,0]])

O_SHAPE_TEMPLATE = ([[5,5],
					[5,5]],)

J_SHAPE_TEMPLATE = ([[3,0,0],
					[3,3,3]],
				   [[0,3],
					[0,3],
					[3,3]],
				   [[3,3,3],
					[0,0,3]],
				   [[3,3],
					[3,0],
					[3,0]])

L_SHAPE_TEMPLATE =([[7,7,7],
					[7,0,0]],
				   [[7,0],
					[7,0],
					[7,7]],
				   [[0,0,7],
					[7,7,7]],
				   [[7,7],
					[0,7],
					[0,7]])

T_SHAPE_TEMPLATE = [[[0,1,0],
					[1,1,1]],
				   [[0,1],
					[1,1],
					[0,1]],
				   [[1,1,1],
					[0,1,0]],
				   [[1,0],
					[1,1],
					[1,0]]]

LS_SHAPE_TEMPLATE = ([[7,7],
					[7,0]],
				   [[7,0],
					[7,7]],
				   [[0,7],
					[7,7]],
				   [[7,7],
					[0,7]])

BRICKS = [S_SHAPE_TEMPLATE,
		  Z_SHAPE_TEMPLATE,
  		  I_SHAPE_TEMPLATE,
  		  O_SHAPE_TEMPLATE,
  		  J_SHAPE_TEMPLATE,
  		  L_SHAPE_TEMPLATE,
  		  T_SHAPE_TEMPLATE]

# QBRICKS = [L_SHAPE_TEMPLATE,
# 		T_SHAPE_TEMPLATE,
# 		J_SHAPE_TEMPLATE]

# BRICKS = [O_SHAPE_TEMPLATE,
# 		I_SHAPE_TEMPLATE]

QBRICKS = [LS_SHAPE_TEMPLATE]
