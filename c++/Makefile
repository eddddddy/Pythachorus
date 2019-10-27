CXX = g++
CXXFLAGS = -std=c++17 -Wall -O3 -g
EXEC = freqs

${EXEC}: main.cc libfixeddatatune.a
	${CXX} ${CXXFLAGS} main.cc -L . -lfixeddatatune -o ${EXEC}
