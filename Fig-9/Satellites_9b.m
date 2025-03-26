% Fig. 9 (b)
startTime = datetime(2025, 3, 12, 14, 22, 0, 'TimeZone', 'UTC');
stopTime = startTime + minutes(3);
sampleTime = 1;

sc = satelliteScenario(startTime, stopTime, sampleTime, 'AutoSimulate', true);
v = satelliteScenarioViewer(sc, "ShowDetails", true);

sat = satellite(sc, './oneweb_tle_2025-03-12T23_00_00Z.txt');

latitude = 50; 
longitude = 160; 
height = 15000000; 
campos(v, latitude, longitude, height);
play(sc);