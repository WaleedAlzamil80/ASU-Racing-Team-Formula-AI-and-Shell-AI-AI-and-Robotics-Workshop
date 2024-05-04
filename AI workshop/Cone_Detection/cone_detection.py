import numpy as np
def detect_cones(h, array, epsilon_bias = 0.1, epsilon_rmse = 0.5, epsilon_radius = 0.1, r=0.05):
    """
    h : hight of the cone

    array : should contain the corrdinates x,y,z at the first 3 columns in the specific order.
            shape : (m, 3) or (m, 4) where m is the number of points(observations)  
            NOTE : I am not interested in the last column
    
    The threshold values:
    epsilon_radius  : the minimum difference in the bias term from the calculations and from the Normal equation
    epsilon_rmse     : the minimum root mean squared error               
    epsilon_radius  : the minimum difference in first and third coefficient 
                        NOTE: maybe you will need to tune this value

    r : radius of the base of the cone (NOT required)
    """
    # prepare the required data
    x_2 = np.square(array[:,0])                                                                                         #(m,1)
    y_2 = np.square(array[:,1])                                                                                         #(m,1)
    z_cap = np.square(array[:,2] - h)                                                                                   #(m,1)
    input_data = np.vstack([x_2,array[:,0],y_2,array[:,1]]).T                                                           #(m,4)
    input_array = np.hstack((input_data,np.ones((input_data.shape[0],1))))                                              #(m,5)

    # Do the calculations
    try:
        weights = np.dot((np.dot(np.linalg.inv(np.dot(input_array.T,input_array)),input_array.T)),z_cap)                #(5,1)
    except:
        weights = np.dot((np.dot(input_array.T, np.linalg.inv(np.dot(input_array,input_array.T)))),z_cap)               #(5,1)

    z_pred_cap = np.dot(input_array,weights)                                                                            #(m,1)
    z_pred = np.sqrt(z_pred_cap) + h                                                                                    #(m,1)

    # Measure all kinds of errors
    rmse = np.sqrt((1/array.shape[0])*np.sum(np.square(z_pred - array[:,2])))                                           #(1,1)
    error_in_the_radius = np.abs((weights[0])-(weights[2]))                                                             #(1,1)
    bias_term_from_calculations = (np.square(weights[1])/(4*weights[0])) + (np.square(weights[3])/(4*weights[2]))       #(1,1)
    bias_error = np.abs((bias_term_from_calculations) - (weights[4]))                                                   #(1,1)

    #set up the conditions and Output the results
    if(bias_error < epsilon_bias) and (rmse < epsilon_rmse) and (error_in_the_radius < epsilon_radius):
        a_x = -weights[1]/(2*weights[0])
        a_y = -weights[3]/(2*weights[2])
        return True, (a_x, a_y)
    else:
        return False
