#ifndef HEADER_H_INCLUDED
#define HEADER_H_INCLUDED

#include "eigen3/Eigen/Dense"
#include <iostream>
#include <vector>

class EKF {
public:

  EKF();
  void filter(Eigen::MatrixXd Z);

private:
  void measurementUpdate(Eigen::MatrixXd Z);
  void statePrediction();

  Eigen::MatrixXd P_; //Initial uncertainty
  Eigen::MatrixXd F_; //Linearized state approximation function
  Eigen::MatrixXd H_; //Jacobian of linearrized measurement function
  Eigen::MatrixXd R_; //Measurement uncertainty
  Eigen::MatrixXd I_; //Identity matrix
  Eigen::MatrixXd u_; //Mean of state function
  Eigen::MatrixXd x_; //Matrix of initial state variables

};

#endif // HEADER_H_INCLUDED
