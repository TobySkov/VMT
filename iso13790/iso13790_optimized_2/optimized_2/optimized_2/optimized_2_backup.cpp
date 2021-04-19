// iso13790.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;




//https://www.cplusplus.com/doc/tutorial/functions/
//Pass inputs by refernce to avoid a local copy.
//Use const to show inputs
//Use infile functions


inline void params(double& H__tr_1, double& H__tr_2, double& H__tr_3, 
				double& Phi__ia, double& Phi__m, double& Phi__st,
				const double& H__ve, double& H__tr_is, const double& H__tr_w, const double& H__tr_ms,
				const double& Phi__int, const double& Phi__sol, const double& A__m, const double& A__t)
{
	//ISO 13790
	//Equations: (C.6), (C.7), (C.8)
	H__tr_1 = 1 / (1 / (H__ve)+1 / (H__tr_is));
	H__tr_2 = H__tr_1 + H__tr_w;
	H__tr_3 = 1 / (1 / (H__tr_2)+1 / (H__tr_ms));


	//ISO 13790
	//Equations: (C.1), (C.2), (C.3)
	Phi__ia = 0.5*Phi__int;
	Phi__m = (A__m / A__t)*(0.5*Phi__int + Phi__sol);
	Phi__st = (1 - (A__m / A__t) - H__tr_w / (9.1*A__t))*(0.5*Phi__int + Phi__sol);


}



inline vector<double> temperatures(const double& Phi__m, const double& Phi__st, const double& Phi__ia, const double& Phi__HC_nd,
	const double& H__tr_em, const double& H__tr_3, const double& H__tr_w, const double& H__tr_1, const double& H__tr_ms,
	const double& H__ve, const double& H__tr_2, const double& H__tr_is,
	const double& theta__e, const double& theta__sup, const double& theta__m_tm1, const double& C__m)
{
	//ISO 13790
	//Equations: (C.4), (C.5)
	double Phi__mtot = Phi__m + H__tr_em * theta__e + \
		H__tr_3*((Phi__st + H__tr_w * theta__e + H__tr_1 * (theta__sup + \
		(Phi__ia + Phi__HC_nd) / (H__ve))) / (H__tr_2));

	double theta__m_t = (theta__m_tm1*(C__m / 3600.0 - (0.5*(H__tr_3 + H__tr_em))) \
		+ Phi__mtot) / (C__m / 3600.0 + (0.5*(H__tr_3 + H__tr_em)));

	double theta__m = 0.5*(theta__m_t + theta__m_tm1);

	double theta__s = (H__tr_ms*theta__m + Phi__st + H__tr_w * theta__e + \
		H__tr_1*(theta__sup + \
		(Phi__ia + Phi__HC_nd) / H__ve)) / (H__tr_ms + H__tr_w + \
			+ H__tr_1);

	double theta__air = (H__tr_is*theta__s + H__ve * theta__sup + Phi__ia + \
		Phi__HC_nd) / (H__tr_is + H__ve);

	vector<double> result = { theta__m_t,  theta__m, theta__s, theta__air };

	return result;
}




vector<double> run_sim() {

	vector<double> theta__air__list;
	theta__air__list.reserve(8760);

	double H__tr_em = 2.5;
	double H__tr_is = 20.5;
	double H__tr_w = 2.5;
	double H__tr_ms = 20.5;
	double A__f = 25.0;
	double C__m = 165000 * A__f;
	double A__m = 2.5*A__f;
	double A__t = 4.5*A__f;

	double setpoint_cooling = 24;
	double setpoint_heating = 20;

	

	double theta__m_tm1 = 22; //Initial value

	vector<double> output_params(6);

	vector<double> output_temperatures(4);

	double Phi__HC_nd_0 = 0;
	double Phi__HC_nd_10 = 10 * A__f;
	double Phi__HC_nd;

	double theta__m_t_0, theta__m_0, theta__s_0, theta__air_0;
	double theta__m_t_10, theta__m_10, theta__s_10, theta__air_10;
	double theta__m_t, theta__m, theta__s, theta__air;

	double theta__air_set;

	double Phi__int = 0;
	double Phi__sol = 0;
	double theta__e = 10;
	double theta__sup = 10;

	double H__ve = 2.5;

	cout << "H__tr_1:" << H__tr_1 << endl;

	double H__tr_1, H__tr_2, H__tr_3, Phi__ia, Phi__m, Phi__st;
	params(H__tr_1, H__tr_2, H__tr_3, Phi__ia, Phi__m, Phi__st,
			H__ve, H__tr_is, H__tr_w, H__tr_ms, Phi__int, Phi__sol, A__m, A__t);

	cout << "H__tr_1:" << H__tr_1 << endl;

	for (int i = 0; i < 8760; i++) {

		output_temperatures = temperatures(Phi__m, Phi__st, Phi__ia, Phi__HC_nd_0,
			H__tr_em, H__tr_3, H__tr_w, H__tr_1, H__tr_ms,
			H__ve, H__tr_2, H__tr_is,
			theta__e, theta__sup, theta__m_tm1, C__m);

		theta__m_t_0 = output_temperatures[0];
		theta__m_0 = output_temperatures[1];
		theta__s_0 = output_temperatures[2];
		theta__air_0 = output_temperatures[3];

		if (setpoint_heating <= theta__air_0 && theta__air_0 <= setpoint_cooling) {

			theta__m_tm1 = theta__m_t_0;
			theta__air__list.push_back(theta__air_0);

		}
		else {

			output_temperatures = temperatures(Phi__m, Phi__st, Phi__ia, Phi__HC_nd_10,
				H__tr_em, H__tr_3, H__tr_w, H__tr_1, H__tr_ms,
				H__ve, H__tr_2, H__tr_is,
				theta__e, theta__sup, theta__m_tm1, C__m);

			theta__m_t_10 = output_temperatures[0];
			theta__m_10 = output_temperatures[1];
			theta__s_10 = output_temperatures[2];
			theta__air_10 = output_temperatures[3];


			if (theta__air_0 < setpoint_heating) {
				theta__air_set = setpoint_heating;
			}
			else if (setpoint_cooling < theta__air_0) {
				theta__air_set = setpoint_cooling;
			}

			Phi__HC_nd = Phi__HC_nd_10 * ((theta__air_set - \
				theta__air_0) / (theta__air_10 - \
					theta__air_0));

			output_temperatures = temperatures(Phi__m, Phi__st, Phi__ia, Phi__HC_nd,
				H__tr_em, H__tr_3, H__tr_w, H__tr_1, H__tr_ms,
				H__ve, H__tr_2, H__tr_is,
				theta__e, theta__sup, theta__m_tm1, C__m);

			theta__m_t = output_temperatures[0];
			theta__m = output_temperatures[1];
			theta__s = output_temperatures[2];
			theta__air = output_temperatures[3];

			theta__m_tm1 = theta__m_t;
			theta__air__list.push_back(theta__air);
		}

	}


	return theta__air__list;
}



int main()
{
	int total_time = 0;

	for (int i = 0; i < 1000; i++) {
		auto start = high_resolution_clock::now();
		vector<double> results = run_sim();
		auto stop = high_resolution_clock::now();
		auto duration = duration_cast<microseconds>(stop - start);
		total_time += duration.count();
	}

	cout << "Avereage time taken by function (1000 runs): "
		<< total_time/1000 << " microseconds" << endl;

}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
