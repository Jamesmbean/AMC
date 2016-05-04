from com.etq.util import Log

## ----------------------------------------------------------------------------

## ----------------------------------------------------------------------------
	
def onOpen():
	## onOpen AIDMOR vier
	#### -----------------------------------------------------------------------
	#### the scope of these valiables are the life of the open form

		#### -----------------------------------------------------------------------
	if thisDocument.isNew():
		myLog("ZZZZZ new AIDMOR Vier Instance ZZZZZZ")
		cat="%s~%s~EVENT~%s" % (company, org,"%")
		parentSF = thisDocument.getSubform("EVENT_TYPE_2_P")  
		mklList = getLeftmostStartingAtDelimiter( "CATEGORY_LOOKUP_P","AIDMOR_CATEGORY","AIDMOR_CATEGORY_ID", cat)
		buildAllTypeLists() # this uses the subform to do its thing
	return
		
def onRefresh():
	return
	
## ----------------------------------------------------------------------------
def myLog( message):
	if chatty:
		Log.info("",message)
	return
	
def isDevelopment():
	return  thisUser.isMember("DEVELOPMENT_P")

def  makeDAOQueryList( datasourceName, param):
	myLog( "makeDAOQuery IN")
	dao = thisApplication.executeQueryFromDatasource( datasourceName, param) 
	list=[]
	debug= "dao.count: %s\n" % dao.count()
	debug+="%s\n" % param
	while dao.next():		## next will start at the first entry and iterate through
		dict = {}
		dict["ID"]= dao.getValue("ID")
		dict["POS"]= dao.getValue("POS")
		dict["DESCRIPTION"]= dao.getValue("DESCRIPTION")
		list.append( dict)
		debug+="ID:%s POS: %s DESCRIPTION:%s\n" % (dict["ID"],dict["POS"], dict["DESCRIPTION"])
	debug+= "list: %s\n" % list	
	myLog(debug)
	myLog( "makeDAOQuery OUT")
	return list

	
def  makeDAOQuery( datasourceName, param):
	myLog( "makeDAOQuery IN")
	dao = thisApplication.executeQueryFromDatasource( datasourceName, param) 
	dict={}
	debug= "dao.count: %s\n" % dao.count()
	debug+="%s\n" % param
	while dao.next():		## next will start at the first entry and iterate through
		dict[dao.getValue("ID")] = dao.getValue("DESCRIPTION")
		debug+="ID:%s DESCRIPTION:%s\n" % (dao.getValue("ID"),dao.getValue("DESCRIPTION"))
	debug+= "dict: %s\n" % dict	
	myLog(debug)
	myLog( "makeDAOQuery OUT")
	return dict

def getLeftmostStartingAtDelimiter( dataSource, table, key,cat):
	myLog("getLeftmostStartingAtDelimiter IN")
	param = {
		"ETQ$APPLICATION":"LOOKUPS",
		"ETQ$TABLE_NAME":table,
		"ETQ$TABLE_KEY": key,
		"ETQ$WHERE_LIKE":  cat,		
		"ETQ$DELIMITER": '~'
		}

	# dict =  makeDAOQuery(dataSource, param)
	list = makeDAOQueryList(dataSource, param)
	myLog("getLeftmostStartingAtDelimiter OUT")

	return list
	
def getRightmostFromLastDelimiter( datasource,table, key, id):
	myLog("getRightmostFromLastDelimiter IN")
	sql = """
	SELECT TESTMKL.TESTMKL_ID , 	
		SUBSTRING_INDEX( TESTMKL.DESCRIPTION ,"ETQ$DELIMITER",-1) DESCRIPTION 
		FROM LOOKUPS.ETQ$TABLE_NAME TESTMKL
	WHERE ETQ$TABLE_NAME.DESCRIPTION LIKE "ETQ$WHERE_LIKE"  
	"""	
	param = {
		"ETQ$TABLE_NAME":table,
		"ETQ$TABLE_KEY": key,
		"ETQ$WHERE_LIKE":  cat,
		"ETQ$DELIMITER": '  "~"  '
	}
	dict =  makeDAOQuery(dataSource, param)
	myLog("getRightmostFromLastDelimiter OUT")
	return dict

def buildCategoryCheckList( mklList, parentSF,queryFieldID):
	myLog("buildCategoryCheckList IN")
	myLog(queryFieldID)
	currentKey =""
	debug=""
				#values = sorted(mklDict.values())  mklList is now a sorted list of dicts
	
	for value in mklList:
		newKey=""
		debug+=" value[DESCRIPTION] %s\n" %(value["DESCRIPTION"])
		list = value["DESCRIPTION"].split('~')
		if len(list)>3:
				newKey= "%s~%s~%s~%s" % (list[0],list[1],list[2],list[3])
			
		myLog(value["DESCRIPTION"])
		debug+="currentKey: <%s>  newKey <%s> NOT EQUAL %s\n" %(newKey, currentKey,(newKey != currentKey))
		recordAlreadyExists = False
		for record in parentSF.getRecords():
			if  newKey == record.getFieldValue( queryFieldID):
				recordAlreadyExists = True
				break
				
		if recordAlreadyExists == True:
			debug += ("record already exists!\n")
		else:
			if  newKey != currentKey:
				currentKey = newKey
				newRecord = parentSF.newRecord()
				newRecord.setFieldValue( queryFieldID , currentKey)
	
	thisDocument.setFieldValue("DEBUG_29_P",debug)
	myLog("buildCategoryCheckList OUT")
	return
	
def loadCategorySubform( category, subformID,queryFieldID):
		myLog("loadCategorySubform IN")
		cat="%s~%s~%s~%s" % (company, org, category, "%")
		myLog(cat)
		parentSF = thisDocument.getSubform(subformID)  
		if parentSF !=None:
			if thisDocument.isNew():
				parentSF.removeAllRecords()
			mklList = getLeftmostStartingAtDelimiter( "CATEGORY_LOOKUP_P","AIDMOR_CATEGORY","AIDMOR_CATEGORY_ID", cat)
			buildCategoryCheckList(mklList, parentSF,queryFieldID)
		myLog("loadCategorySubform OUT")
		return
		

		
def  buildLocationList( notificationIDS, locationsAsText):
	myLog("buildLocationList IN")
	debug=''
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
		debug += "%s %s %s %s\n" % (location, locationProfile.getDisplayName(), locationProfile.getName(),locationProfile.getHierarichicalName())
	  
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

	notifications="%s\n%s\n"  % (thisUser.getID(), '4825')   			# the 4825 is the Group ID for AMC-Oair Distro
	for (key,value) in regions.iteritems():
		for id in value:
			notifications+="%s\n" % id
	  
	thisDocument.getField(notificationIDS).setValue( notifications)
	thisDocument.setFieldValue(locationsAsText, cities)
	debug += "Cities: %s\n" % cities
	myLog(debug)
	myLog("buildLocationList OUT")
	return
	
def slurpSubform( attr):
	myLog( "slurpSubform in")
	content =""
	subformID = attr[0]
	
		# section category :( SubformID, category, query string, subcategory, other)
	subform = thisDocument.getSubform( subformID)
	
	if (subform!=None) and (subform.size() >0):
		content+="</br><b>%s</b></br>" % subform.getDisplayName()
		catID =attr[1]	
		
		for record in subform.getRecords():
			category = record.getField(catID).getDisplayText()
			subcategoryCB = record.getField(attr[3])
			other = record.getField(attr[4])
			if len(category)>0:	
				content+="</br>%s" % category
				query = record.getField(attr[2])
				str = subcategoryCB.getDisplayText().replace(";","</li><li>")
				if len(str)>0:
					content+="<ul ><li>%s</li></ul>" % (str)
					other = other.getValue()
					if len(other)>0:
						content+="<div style='text-indent:50px;'>Description: %s</div>" % other
			else:		# if the parent CB is off then reset the children
				subcategoryCB.clear()
				other.setValue("")

	else:
		myLog("None or empty subform")
	content+="</br>"
	myLog( "slurpSubform OUT")
	return content
	
def clearAllFormFields():
	myLog("clearAllFormFields IN")
	for key,list in dictSubformAttributes.iteritems():
		subform = thisDocument.getSubform(list[0])  
		if subform !=None:
			for record in subform.getRecords():
				count = len( record.getFieldValues(list[1]) )
				if count  ==0:
					record.setFieldValues(list[3],[])
	myLog("clearAllFormFields OUT")
	return
			
def clearLocationFields( ):
	locationType = thisDocument.getField("LOCATION_TYPE_2_P").getDisplayText()
	clearList =()
	if locationType =="Scene":
		clearList =(
			"EVENT_LOCATION_5_P"
			,"HOSPITAL_NAME_2_P"
			,"AMC_BASE_1_P"
			,"AIRPORT_NAME_P"
		)
	if locationType =="Base":
		clearList =(
			"LATTITUDE_P"
			, "LONGITUDE_P"
			,"LOCATION_OWNER_S_NAME_P"
			,"LOCATION_OWNER_NUMBER_P"
			,"LOCATION_IS_SECURE_1_P"
			,"HOSPITAL_NAME_2_P"
			,"AMC_BASE_1_P"
			,"AIRPORT_NAME_P"
			,"DESCRIPTION_8_P"
			,"CITY_2_P"
			,"STATE_3_P"
		)
	if locationType =="Hospital":
		clearList = (
			"EVENT_LOCATION_5_P"
			,"LATTITUDE_P"
			, "LONGITUDE_P"
			,"AMC_BASE_1_P"
			,"AIRPORT_NAME_P"
		)
	if locationType =="Airport":
		clearList = (
			"EVENT_LOCATION_5_P"
			,"LATTITUDE_P"
			, "LONGITUDE_P"
		)
	if locationType =="Other":
		clearList = (
			"EVENT_LOCATION_5_P"
			,"LOCATION_IS_SECURE_1_P"
			,"HOSPITAL_NAME_2_P"
			,"AIRPORT_NAME_P"

		)	
	if locationType =="N/A":
		clearList = (
				"EVENT_LOCATION_5_P"
				,"LATTITUDE_P"
				, "LONGITUDE_P"
				,"LOCATION_OWNER_S_NAME_P"
				,"LOCATION_OWNER_NUMBER_P"
				,"LOCATION_IS_SECURE_1_P"
				,"HOSPITAL_NAME_2_P"
				,"AMC_BASE_1_P"
				,"AIRPORT_NAME_P"
				,"DESCRIPTION_8_P"
				,"CITY_2_P"
				,"STATE_3_P"
			)	
	for fldID in clearList:
		thisDocument.setFieldValue(fldID, "")
		
def gotoNextTab( ):
	myLog("gotoNextTab")
	nextTab ={	"BASIC_TAB":"EVENT_TYPE_TAB"
		,	"EVENT_TYPE_TAB":"THREAT_TAB"
		,	"THREAT_TAB":"ERROR_TAB"
		,	"ERROR_TAB":"EVENT_DESCRIPTION_TAB"
		,	"EVENT_DESCRIPTION_TAB":"SUMMARY_TAB"
		,	"SUMMARY_TAB":"SUMMARY_TAB" 
		,"  ALL_TABS_TAB":"  ALL_TABS_TAB"}	
	thisTab = thisDocument.getActiveTabDesignName()
	if thisTab !="":
		thisDocument.gotoTab( nextTab[thisTab])
	else:
		myLog("Hmm got no tab whats up with that?")
	
def gotoPreviousTab():
	myLog("gotoPreviousTab")
	previousTab ={	"BASIC_TAB":"BASIC_TAB"
		,	"EVENT_TYPE_TAB":"BASIC_TAB"
		,	"THREAT_TAB":"EVENT_TYPE_TAB"
		,	"ERROR_TAB":"THREAT_TAB"
		,	"EVENT_DESCRIPTION_TAB":"ERROR_TAB"
		,	"SUMMARY_TAB":"EVENT_DESCRIPTION_TAB" 
		, 	"ALL_TABS_TAB":"  SUMMARY_TAB"}	
	thisTab = thisDocument.getActiveTabDesignName()
	if thisTab !="":
		thisDocument.gotoTab( previousTab[thisTab])
	else:
		myLog("Hmm got no tab whats up with that?")
		
###

def purgeEmptyRecords():
	myLog("purgeEmptyRecords IN")
	debug = ""
						# section category :( SubformID, category, query string, subcategory, other)
	for cat, value  in dictSubformAttributes.iteritems():	# instantiated in onOpen 
		subFormID = value[0]
		debug+= "Subform is %s\n" % subFormID
		categoryID = value[1]
		debug+="categoryID is %s\n" % (categoryID)
		sf = thisDocument.getSubform( subFormID)
		if sf != None:
			debug+="got sf  its size is %s" % sf.size()
			records = sf.getRecords()
			debug+="... sf has %s records\n" % len(records)
			
			for record in records:
				count =   len(  record.getFieldValues( categoryID))
				debug+="Checkbox items selected (count) is: %s" % count 
				fld = record.getField(categoryID)
				prompt = record.getFieldPrompt(categoryID)
				if  count ==0:	
					debug+="Remove ID %s  " %  categoryID
					debug+="%s is %s NOT checked\n" % ( prompt,   fld.getDisplayText() )
					sf.removeRecord( record.getRecordOrder())		
				else:
					debug+="%s is %s checked\n" % (prompt,   fld.getDisplayText() )
		else:
			debug += "NO sf found"
	#myLog( debug)
	#thisDocument.setFieldValue("DEBUG_29_P",debug)
	myLog("purgeEmptyRecords OUT")
	return
 
def buildAllTypeLists():
	myLog("buildAllTypeLists IN")
						# section category :( SubformID, category, query string, subcategory, other)
	for key,value  in dictSubformAttributes.iteritems():	# instantiated in onOpen 
		myLog(key)
		loadCategorySubform(key,value[0],value[2]) #subformID and query string
	myLog("buildAllTypeLists OUT")
	return

def  getCategoryTypesAsText( sfID, catID):
	myLog( "getCategoryTypesAsText IN")
	categoryText =""
	subform = thisDocument.getSubform(  sfID)  
	if subform != None:
		myLog( "Got subform")
		for record in subform.getRecords():
			fld = record.getField(  catID )
			if fld != None:
				category = fld .getDisplayText()
				debug= "CAT %s" % category
				myLog(debug)
				if  category != None and category != "":
					if categoryText != "":
						categoryText +=", "
					categoryText += category
			else:
				myLog( "FAILED to get CATEGORY field")

			debug = "categoryText is %s" % categoryText
			myLog(debug)
	else:
		myLog( "FAILED to get subform")
	if categoryText =="":
		categoryText = "None selected"
	myLog( categoryText)
	myLog( "getCategoryTypesAsText OUT ")
	return categoryText
	
def submitForm():
	myLog("submitForm IN")
	# 4923  AIDMOR_TEST_P
	debug=""
	eMailsLst = []
	UsersIDs =[]    
	purgeEmptyRecords()
	thisDocument.save()
	# buildSummary()
	buildSummaryToo()
	summary = thisDocument.getField("EVENT_SUMMARY_P").getValue()
	officialPurposes= """
	<p class="official""></br><b>Official Use:</b></br>This report and any files or text attached to it are intended only for official	use by Air Methods Corporation and may not be transmitted, copied or
			otherwise disclosed to parties outside of Air Methods Corporation without specific authorization by an Air Methods Corporation Division President or 	their designee.</p>
	"""
	summary+=officialPurposes
	StrUsersIDs = userManager.convertToUsers(["AIDMOR_TEST_P"])
	 #StrUsersIDs = userManager.getUsersIDs( userManager.convertToUsers([4923]))
	for usersID in StrUsersIDs:
		email = eccProfileManager.getUserProfile(Rstring.toInteger(usersID)).getEmail()
		eMailsLst.append(email)
		UsersIDs.append(Rstring.toInteger(usersID))
	  
	eMailsLst.append( thisUser.getEmail())
	mailObj = PublicMail()
	mailObj.setToEmails(eMailsLst)
	mailObj.setToUserIDs(UsersIDs)
	
	loc = thisDocument.getField("ETQ$LOCATIONS").getDisplayText() 
	id = thisDocument.getFieldValue("ETQ$NUMBER") 	#getID()
	sfID =dictSubformAttributes["EVENT"][0]
	catID =dictSubformAttributes["EVENT"][1]
	catText =""
	catText = getCategoryTypesAsText( sfID, catID   )
	if catText=="":
		catText="--"
	subject = 'TEST AIDMOR %s Loc: %s %s'  % (id, loc, catText  )  #TEST AIDMOR 1234 |(Emp Base Location) | (Event Type List)
	mailObj.setSubject(subject)  # AIDMOR 000000 Loc: Lone Tree
	mailObj.setBody(summary)
	mailObj.setPublicDocument(thisDocument)
	mailObj.setSenderUserID(Rstring.toInteger(thisUser.getID()))
	mailObj.setSenderEmail(thisUser.getEmail())
	PublicMailSender.sendEmail(mailObj)
	dateDue = Rdate.currentDateTime ()
	phase = thisDocument.getPhase()
	phase.route("COMPLETE_10_P",1 )
	thisDocument.close()
	thisAction.goToLastAccessedTab() 
	myLog("submitForm OUT")
	return
	
def validatePhoneNumber( phone):
	newPhone=""
	for char in phone:		# remove any extra stuff non numerics
		if char >="0" and char <="9":
			newPhone+="%c" % char
	if len(newPhone)>=10:
		newPhone = "(%c%c%c) %c%c%c-%c%c%c%c" % (newPhone[0],newPhone[1],newPhone[2],newPhone[3],newPhone[4],newPhone[5],newPhone[6],newPhone[7],newPhone[8],newPhone[9])
	else:
		newPhone=""
	return newPhone
	
def validateLatLong( lat):
	newLat =""
	for i, char in enumerate(lat):
		if i == 0:
			if char in "+-":
				newLat +="%c" % char
			else:
				newLat +="%c" % "+"
		if (char >="0" and char <="9") :
			newLat+="%c" % char
	if len(newLat)>=6:
		newLat = "%c%c%c%c.%c%c" % (newLat[0],newLat[1],newLat[2],newLat[3],newLat[4],newLat[5])
	else:
		newLat=""
	return newLat
	
def getCategoryCheckBoxen( queryField):
	debug = "getCategoryCheckBoxen In - %s " % queryField
	myLog(debug)
	sql="""
	SELECT CAT.AIDMOR_CATEGORY_ID AIDMOR_CATEGORY_ID, 
	SUBSTRING_INDEX( CAT.DESCRIPTION ,'~',-1)    DESCRIPTION
	FROM LOOKUPS.AIDMOR_CATEGORY CAT
	WHERE CAT.ETQ$IS_DISABLED = 0	 
	"""
	emptySQL = 	"""
	SELECT CAT.AIDMOR_CATEGORY_ID AIDMOR_CATEGORY_ID, 
	SUBSTRING_INDEX( CAT.DESCRIPTION ,'~',-1)    DESCRIPTION
	FROM LOOKUPS.AIDMOR_CATEGORY CAT
	WHERE CAT.AIDMOR_CATEGORY_ID is NULL
	"""
	queryValue = thisSubformRecord.getFieldValue(queryField)
	debug = "queryValue is <%s>" % queryValue
	myLog(debug)
	if queryValue!=None :
		whereClause = "AND  CAT.DESCRIPTION LIKE '%s' " % queryValue
		sql+=whereClause+"   ORDER BY CAT.ETQ$RECORD_ORDER"
		if queryValue!="":
			thisField.setQueryParameter("VAR$USER", sql)
		else:
			thisField.setQueryParameter("VAR$USER", emptySQL)
		
	myLog(sql)
	myLog("getCategoryCheckBoxen Out")
	return
		
def getSubCategoryCheckBoxen( queryField):
	debug = "getSubCategoryCheckBoxen In - %s " % queryField
	myLog(debug)

	sql="""
	SELECT CAT.AIDMOR_CATEGORY_ID AIDMOR_CATEGORY_ID, 
	SUBSTRING_INDEX( CAT.DESCRIPTION ,'~',-1)    DESCRIPTION
	FROM LOOKUPS.AIDMOR_CATEGORY CAT
	WHERE ETQ$IS_DISABLED = 0
	"""
	queryValue = thisSubformRecord.getFieldValue(queryField)
	if queryValue!=None:
		whereClause = "AND  CAT.DESCRIPTION LIKE '%s~" % queryValue
		sql+=whereClause+"%'   ORDER BY CAT.ETQ$RECORD_ORDER"
		thisField.setQueryParameter("VAR$USER", sql)
	myLog(sql)
	myLog("getSubCategoryCheckBoxen Out")
	return
	
def redux():
	users=[thisUser]

	dt = Rdate.currentDateTime()
	dt = Rdate.adjustDate(dt,0,0,2,0,0,0)
	#thisPhase.route("START_16_P","redux",-1,False)
	thisPhase.route("START_16_P",dt, users, users,"redux",-1)
	buildAllTypeLists()
	
	return
	
def isEvent():
	return True	
