// iso13790_optimized.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <vector>
#include <chrono>

using namespace std;
using namespace std::chrono;


vector<double> occ_sch() 
{
	vector<double> occ_sch_list;
	occ_sch_list.reserve(8760);

	for (int j = 0; j < 52; j++) { //52 weeks

		for (int i = 0; i < 5; i++) { // 5 weekdays in week
			occ_sch_list.insert(occ_sch_list.end(), { 0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0 });
		}
		for (int i = 0; i < 2; i++) { // 2 weekenddays in week
			occ_sch_list.insert(occ_sch_list.end(), { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 });
		}
	}

	//One more day to add up to 8760 hours (52*7 = 364)
	occ_sch_list.insert(occ_sch_list.end(), { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 });

	return occ_sch_list;

}

vector<double> before_runtime(double H__ve,
	double H__tr_is, double H__tr_w, double H__tr_ms, double H__tr_em,
	double A__m, double A__t, double C__m)
{
	//The function should be called two times, once for each value of H__ve

	//Equations: (C.6), (C.7), (C.8)
	double H__tr_1 = 1 / (1 / (H__ve)+1 / (H__tr_is));
	double H__tr_2 = H__tr_1 + H__tr_w;
	double H__tr_3 = 1 / (1 / (H__tr_2)+1 / (H__tr_ms));


	//Division operators used in other functions
	double tmp0 = A__m / A__t;
	double tmp1 = H__tr_w / (9.1*A__t);
	double tmp2 = H__tr_3 / H__tr_2;
	double tmp3 = 1 / H__ve;

	double local_tmp = C__m / 3600;
	double local_tmp2 = 0.5*(H__tr_3 + H__tr_em);
	double tmp4 = local_tmp - local_tmp2;
	double tmp5 = 1 / (local_tmp + local_tmp2);

	double tmp6 = 1 / (H__tr_ms + H__tr_w + H__tr_1);
	double tmp7 = 1 / (H__tr_is + H__ve);

	double tmp8 = H__tr_w;
	double tmp9 = H__tr_em;
	double tmp10 = H__tr_ms;
	double tmp11 = H__ve;
	double tmp12 = H__tr_is;

	vector<double> return_vector = { tmp0, tmp1, tmp2, tmp3, tmp4, tmp5, tmp6, 
									tmp7, tmp8, tmp9, tmp10, tmp11, tmp12 };

	return return_vector;
}


vector<double> at_runtime(double Phi__int, double Phi__sol, double Phi__HC_nd,
							double theta__e, double theta__sup, double theta__m_tm1,
							vector<double> params) 
{
	double Phi__ia = 0.5*Phi__int;
	double Phi__m = params[0] * (0.5*Phi__int + Phi__sol);
	double Phi__st = (1 - params[0] - params[1])*(0.5*Phi__int + Phi__sol);


	//ISO 13790
	//Equations: (C.4), (C.5)
	double local_tmp = Phi__st + params[8] * theta__e + \
		params[8] * (params[3] * (Phi__ia + Phi__HC_nd) + theta__sup);

	double Phi__mtot = Phi__m + params[9] * theta__e + params[2] * local_tmp;

	double theta__m_t = (theta__m_tm1*params[4] - Phi__mtot)*params[5];


	//ISO 13790
	//Equations: (C.9), (C.10), (C.11)
	double theta__m = 0.5*(theta__m_t + theta__m_tm1);

	double theta__s = (params[10]*theta__m + local_tmp)*params[6];

	double theta__air = (params[12]*theta__s + params[11] * theta__sup + \
		Phi__ia + Phi__HC_nd)*params[7];


	vector<double> return_vector = { theta__m_t, theta__m, theta__s, theta__air };

	return return_vector;
}




vector<double> run_sim() {

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

	vector<double> output_params;
	output_params.reserve(6);

	vector<double> output_temperatures;
	output_temperatures.reserve(6);

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

	double H__ve;
	
	//Determine the two values of H__ve and corresponding parameters.




	for (int i = 0; i < 8760; i++)
	{
		//Start by setting solar gain, internal heat gain, external temperature and supply temperature.
		

	}


}

int main()
{

	auto start = high_resolution_clock::now();
	vector<double> results = run_sim();
	auto stop = high_resolution_clock::now();

	auto duration = duration_cast<microseconds>(stop - start);

	cout << "Time taken by function: "
		<< duration.count() << " microseconds" << endl;

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
