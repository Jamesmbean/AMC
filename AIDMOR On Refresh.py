## AIDMORE onRefresh


currentTab = thisDocument.getActiveTabDesignName()
if currentTab == "ALL_TABS_TAB" or currentTab == "SUMMARY_TAB":
	buildSummary()  # this is in a resource file

# mostly stolen from the OAIR onRefresh
# figure out the appropriate management groups for the location
locations = thisDocument.getEncodedFieldValues("ETQ$LOCATIONS")

regionKey ={"Region 01" :(4298, 4298,4829),
    "Region 02" :(4303, 4302,4828),
    "Region 03" :(4306, 4305,4830),
    "Region 04" :(4310, 4309,4831),
    "Region 05" :(4314, 4313,4832),
    "Region 06" :(4318, 4317,4833),
    "Region 07" :(4322, 4321,4834),
    "Region 08" :(4326, 4325,4835),
    "Region 09" :(4330, 4329,4836),
    "Region 10" :(4336, 4333,4837),
    "Region 11" :(4339, 4338,4838),
    "Region 12" :(4343, 4342,4839),
    "other":(700,0)}
cities=""
regions={}

for location in locations:
	locationProfile = eccProfileManager.getLocationProfile(location)
	region = locationProfile.getHierarichicalName().split()
	debug = debug + "%s %s %s %s\n" % (location, locationProfile.getDisplayName(), locationProfile.getName(),locationProfile.getHierarichicalName())
  
	city = locationProfile.getHierarichicalName().split(':')
  # now city is just the region info toss the rest
	city = city[0].strip()
	debug+="<%s>\n" % city
	# build a unique list of regions
	if city in regions:
		debug += "<%s> already in regions.\n" % city
	else:
		debug+="not in regions\n"
   # is it a key we are familiar with 
	if city in regionKey:
		regions[city] = regionKey[ city] 
		debug+= "%s is a listed regionKey\n" % city
	else:
		if 'other' not in regions:
			regions['other'] = regionKey['other']
			debug += "Could :not find <%s> in regionKey. Used Other.\n" % city
		else:
			debug += "Could :not find <%s> in regionKey. Other already sexists.\n" % city
  
  # 818 1125 1125_P Region 02 : ANCHORAGE, AK : Wolf Lake, AK - Fuel Facility (Providence Alaska Medical Center)
	city = locationProfile.getHierarichicalName().split(':')
  # strip off any after comments besides city,state
	city = city[len(city)-1].split('-')
	cities += "%s; " % city[0]

debug += " The length of regions is %s\n" % len(regions)
  # the 4825 is the Group ID for AMC-Oair Distro
  
notifications="%s\n%s\n"  % (thisUser.getID(), '4825')
for (key,value) in regions.iteritems():
	for id in value:
		notifications+="%s\n" % id
  
thisDocument.getField("NOTIFICATION_IDS_P").setValue( notifications)
thisDocument.setFieldValue("LOCATIONS_AS_TEXT_P", cities)
debug += "Cities: %s\n" % cities


currentPhase = thisPhase.getName()
debug+=currentPhase

thisDocument.getField("DEBUG_26_P").setValue(debug)