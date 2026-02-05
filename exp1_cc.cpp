#include <iostream>
using namespace std;
 
int main() {
    int t;
    cin >> t;
 
    while(t--) {
        int n;
        cin>>n;
 
        int count = 0;
 
        for (int i = 1;i<=n/i;i++){
            if(n%i==0){
                count++;
                if(i!=n/i)
                    count++;
            }
        }
        cout << count << endl;
    }
    return 0;
}