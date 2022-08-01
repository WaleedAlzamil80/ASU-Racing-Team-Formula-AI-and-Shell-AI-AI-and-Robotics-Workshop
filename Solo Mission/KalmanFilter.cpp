// KALMAN FILTER

#include <iostream>
#include <math.h>

using namespace std;

double kalmanFilter(double mu, double sigma2, double x)
{
    //Use mu, sigma2 (sigma squared), and x to code the 1-dimensional Gaussian
    double prob = 1.0 / sqrt(2.0 * M_PI * sigma2) * exp(-0.5 * pow((x - mu), 2.0) / sigma2);
    cout << "1-D Gaussian Value:" << prob << endl;
    return prob;
}

int main()
{
    double mu, sigma2, x;
    cout << "Enter the values of mu, sigma2 and x respectively:" << endl;
    cin >> mu >> sigma2 >> x;
    cout << kalmanFilter(mu, sigma2, x) << endl;
    return 0;
}

