#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <string>

#include "pitch.h"
#include "score.h"

int main(int argc, char* argv[]) {

    if (argc < 2) return 1;

    std::string filepath = argv[1];
    std::ifstream ifs{filepath};

    Score score;
    std::string line;
    while (std::getline(ifs, line)) {
        std::istringstream iss{line};
        int p, o, d, b;
        iss >> p >> o >> d >> b;
        score.add(EPitch{static_cast<Pitch>(p), o}, d, b);
    }

    score.calculateFreqs();

    std::ofstream ofs{filepath + "_tuned"};
    ofs << std::setprecision(17) << std::fixed;
    for (auto it = score.nbegin(); it != score.nend(); ++it) {
        Note n = (*it);
        ofs << static_cast<int>(n.pitch.pitch.pitch) << " "
            << n.pitch.pitch.octave << " "
            << n.duration << " "
            << n.startBeat << " "
            << n.pitch.freq << std::endl;
    }
}
