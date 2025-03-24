startTime = datetime(2025, 1, 29, 22, 50, 0, 'TimeZone', 'UTC');
stopTime = startTime + minutes(1);
sampleTime = 1;

sc = satelliteScenario(startTime, stopTime, sampleTime, 'AutoSimulate', false);
v = satelliteScenarioViewer(sc, "ShowDetails", false);

% websave('./starlink.tle', 'https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle');
sat = satellite(sc, './starlink.tle');

latitude = 50; 
longitude = 160; 
height = 15000000; 
campos(v, latitude, longitude, height);
