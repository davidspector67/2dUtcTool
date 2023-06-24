default: main.py
	@ python3.9 main.py

build_mac: ./Parsers/philips_rf_parser.c
	gcc -c -Wall -Wpedantic ./Parsers/philips_rf_parser.c
	mv philips_rf_parser.o ./Parsers/philips_rf_parser.o
	gcc -o ./Parsers/philips_rf_parser ./Parsers/philips_rf_parser.o
