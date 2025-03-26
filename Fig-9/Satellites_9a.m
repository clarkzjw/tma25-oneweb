% Fig. 9 (a)
startTime = datetime(2025, 3, 13, 13, 18, 0, 'TimeZone', 'UTC');
stopTime = startTime + minutes(3);
sampleTime = 1;

sc = satelliteScenario(startTime, stopTime, sampleTime, 'AutoSimulate', true);
v = satelliteScenarioViewer(sc, "ShowDetails", true);

sat = satellite(sc, './oneweb_tle_2025-03-12T23_00_00Z.txt');

dish = groundStation(sc, "Latitude", 42.014, "Longitude", -93.651, "Name", "OneWeb UT");
ClewistonGS = groundStation(sc, "Latitude", 26.74865, "Longitude", -81.04928, "Name", "Clewiston SNP");
SouthburyGS = groundStation(sc, "Latitude", 41.452761, "Longitude", -73.288563, "Name", "Southbury SNP");
SantaPaulaGS = groundStation(sc, "Latitude", 34.40218, "Longitude", -119.07341, "Name", "Santa Paula SNP");
AshburnPoP = groundStation(sc, "Latitude", 39.016363, "Longitude", -77.459023, "Name", "Ashburn PoP");

latitude = 42; 
longitude = -93; 
height = 10000000; 
campos(v, latitude, longitude, height);

play(sc);
