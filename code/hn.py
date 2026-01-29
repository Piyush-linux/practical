Hop.h
// hop.h
#include <iostream>
using namespace std;

class neuron {
protected:
    int activation;
    friend class network;
public:
    int weightv[4];
    neuron() {};
    neuron(int *j);
    int act(int, int*);
};

class network {
public:
    neuron nrn[4];
    int output[4];
    int threshld(int);
    void activation(int j[4]);
    network(int*,int*,int*,int*);
};



Hop.cpp
// hop.cpp
#include "hop.h"

neuron::neuron(int *j) {
    int i;
    for (i = 0; i < 4; i++) {
        weightv[i] = *(j + i);
    }
}

int neuron::act(int m, int *x) {
    int i;
    int a = 0;
    for (i = 0; i < m; i++) {
        a += x[i] * weightv[i];
    }
    return a;
}

int network::threshld(int k) {
    if (k >= 0) return 1;
    else return 0;
}

network::network(int a[4], int b[4], int c[4], int d[4]) {
    nrn[0] = neuron(a);
    nrn[1] = neuron(b);
    nrn[2] = neuron(c);
    nrn[3] = neuron(d);
}

void network::activation(int *patrn) {
    int i, j;
    for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
            cout << "\n nrn[" << i << "].weightv[" << j << "] is " << nrn[i].weightv[j];
        }
        nrn[i].activation = nrn[i].act(4, patrn);
        cout << "\nactivation is " << nrn[i].activation;
        output[i] = threshld(nrn[i].activation);
        cout << "\noutput value is " << output[i] << "\n";
    }
}

int main() {
    int patrn1[] = {1,0,1,0}, i;
    int wt1[] = {0,-3,3,-3};
    int wt2[] = {-3,0,-3,3};
    int wt3[] = {3,-3,0,-3};
    int wt4[] = {-3,3,-3,0};

    cout << "\nTHIS PROGRAM IS FOR A HOPFIELD NETWORK WITH A SINGLE LAYER OF";
    cout << "\n4 FULLY INTERCONNECTED NEURONS. THE NETWORK SHOULD RECALL THE";
    cout << "\nPATTERNS 1010 AND 0101 CORRECTLY.\n";

    network h1(wt1, wt2, wt3, wt4);
    h1.activation(patrn1);
    for (i = 0; i < 4; i++) {
        if (h1.output[i] == patrn1[i]) cout << "\n pattern= " << patrn1[i] << " output = " << h1.output[i] << " component matches";
        else cout << "\n pattern= " << patrn1[i] << " output = " << h1.output[i] << " discrepancy occurred";
    }

    cout << "\n\n";
    int patrn2[] = {0,1,0,1};
    h1.activation(patrn2);
    for (i = 0; i < 4; i++) {
        if (h1.output[i] == patrn2[i]) cout << "\n pattern= " << patrn2[i] << " output = " << h1.output[i] << " component matches";
        else cout << "\n pattern= " << patrn2[i] << " output = " << h1.output[i] << " discrepancy occurred";
    }
    return 0;
}
