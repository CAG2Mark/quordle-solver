#include <vector>
#include <map>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;

const string fname = "guess_table";

map<string, map<string, unsigned char> *> guess_table;
bool first_init = false;

// pre-allocate
map<string, unsigned char> pre_tables[2314];
    

class Solver {
public:
    Solver(int N) : N(N) {
        fstream file(fname, ios::in);

        string line, word;

        bool first = true;

        if (first_init || !file.is_open()) return;

        for (int i = 0; getline(file, line); ++i) {
            stringstream str(line);
            string cur_word = "";

            for (int j = 0; getline(str, word, ',') && j <= 2314; ++j) {

                // printf("%d %d\n", i, j);
                if (i == 0 && j == 0) continue;
                if (i == 0) {
                    guess_table[word] = &pre_tables[j-1];
                    continue;
                }
                // i >= 1

                if (j == 0) {
                    cur_word = word;
                    continue;
                }

                pre_tables[j-1][cur_word] = stoi(word, 0, 3);
            }
        }
        first_init = true;
    }
private:
    int N;
};

int main() {
    Solver s(1);
    printf("%d\n", (*guess_table["cigar"])["aahed"]);
}