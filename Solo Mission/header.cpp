EKF::EKF() {
  double meas[5] = {1.0, 2.1, 1.6, 3.1, 2.4};
  x_.resize(2, 1);
  P_.resize(2, 2);
  u_.resize(2, 1);
  F_.resize(2, 2);
  H_.resize(1, 2);
  R_.resize(1, 1);
  I_.resize(2, 2);
  Eigen::MatrixXd Z(1, 1);
  for(int i = 0; i < 5; i++){
    Z << meas[i];
    measurementUpdate(Z);
    //statePrediction();
  }
}

void EKF::measurementUpdate(Eigen::MatrixXd Z){
  //Calculate measurement residual
  Eigen::MatrixXd y = Z - (H_ * x_);
  Eigen::MatrixXd S = H_ * P_ * H_.transpose() + R_;
  Eigen::MatrixXd K = P_ * H_.transpose() * S.inverse();

  //Calculate posterior state vector and covariance matrix
  x_ = x_ + (K * y);
  P_ = (I_ - (K * H_)) * P_;
}

void EKF::statePrediction(){
  //Predict next state vector
  x_ = (F_ * x_) + u_;
  P_ = F_ * P_ * F_.transpose();
}

void EKF::filter(Eigen::MatrixXd Z){
  measurementUpdate(Z);
  statePrediction();
}
