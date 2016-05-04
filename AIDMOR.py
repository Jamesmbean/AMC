from com.etq.util import Log

## ----------------------------------------------------------------------------
def onRefresh():
	return
	
def onOpen():
	return
## ----------------------------------------------------------------------------
def myLog( message):
	if chatty:
		Log.info("",message)
	return
	
def isDevelopment():
	return  thisUser.isMember("DEVELOPMENT_P")

def  makeDAOQueryList( datasourceName, param):
	myLog( "makeDAOQueryList IN")
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
	myLog( "makeDAOQueryList OUT")
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
	#myLog(debug)
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
	debuig = "buildCategoryCheckList IN"
	debug += " \nquery fieldID is %s\n"  % queryFieldID
	myLog(debug)

	currentKey =""
				#values = sorted(mklDict.values())  mklList is now a sorted list of dicts
	
	for value in mklList:
		newKey=""
		debug+=" value[DESCRIPTION] %s\n" %(value["DESCRIPTION"])
		list = value["DESCRIPTION"].split('~')
		if len(list)>3:
				newKey= "%s~%s~%s~%s" % (list[0],list[1],list[2],list[3])
			
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
	
	#thisDocument.setFieldValue("DEBUG_29_P",debug)
	myLog( debug)
	myLog("buildCategoryCheckList OUT")
	return
	
def loadCategorySubform( category, subformID,queryFieldID):
		myLog("loadCategorySubform IN")

		parentSF = thisDocument.getSubform(subformID)  
		if parentSF !=None:
			if thisDocument.isNew():
				parentSF.removeAllRecords()
			#mklList = getLeftmostStartingAtDelimiter( "CATEGORY_LOOKUP_P","AIDMOR_CATEGORY","AIDMOR_CATEGORY_ID", cat)
			mklList = getAIDMORCategory( appSpace, dataSource, company, org, category)
			buildCategoryCheckList2(mklList, parentSF,queryFieldID)
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
	
		# section category :( SubformID, category, query string, sub , other)
	subform = thisDocument.getSubform( subformID)
	
	if (subform!=None) and (subform.size() >0):
		content+="<h3>%s</h3>" % subform.getDisplayName()
		catID =attr[1]	
		#content +="<ul class='cat'>"
		for record in subform.getRecords():
			category = record.getField(catID).getDisplayText()
			subcategoryCB = record.getField(attr[3])

			if len(category)>0:	
				content+="<div class='cat'>- %s</div>" % category
				if "OTHER" in category.upper():
					other = record.getFieldValue(attr[5])
					content+=" <div style='cat'>Other description: %s</div>" % other
				query = record.getField(attr[2])
				str = subcategoryCB.getDisplayText().replace(";","</li><li>")
				if len(str)>0:
					content+="<ul class='sub'><li>%s</li></ul>" % (str)
					other = record.getField(attr[4]).getValue()
					if len(other)>0:
						content+="<div style='sub'>Other description: %s</div>" % other
			else:		# if the parent CB is off then reset the children
				subcategoryCB.clear()
				record.getField(attr[4]).setValue("")
		#content+="</ul>"
	else:
		myLog("None or empty subform")
	content+="</br></br>"
	myLog( "slurpSubform OUT")
	return content

def buildDocumentURL():
	applicationName = thisApplication.getName()
	formName= thisDocument.getFormName()
	keyName = "AIDMOR_VIER_ID" 
	keyValue = thisDocument.getID()
	etqNumber = thisDocument.getFieldValue("ETQ$NUMBER") 
	
	URL="<a class='AIDMOR' href='https://airmethods.etq.com/reliance_prod/reliance?ETQ$CMD=CMD_OPEN_DOC&ETQ$APPLICATION_NAME=%s&ETQ$FORM_NAME=%s&ETQ$KEY_NAME=%s&ETQ$KEY_VALUE=%s' > AIDMOR %s</a>" % (applicationName, formName, keyName,keyValue,etqNumber )
	return URL

defaultPrompt ={
		"BRIEF_EVENT_DESCRIPTION_P":"Brief Description"
	}

	
def slurpFieldList( fieldList):
	summary = ""

	for label, fieldList  in fieldList.iteritems():
		summary+="</br><b>%s</b></br>" % label
		for li in fieldList:
			for field, displayText in li.iteritems():
				prompt=""
				fd = thisDocument.getField(field)
				if fd != None:
					if field in defaultPrompt:
						prompt = defaultPrompt[field]
					else:
						prompt = fd.getPrompt()
					if displayText==1:
						if fd.getValue() !=None:
							summary+="<div><b>%s:</b> %s</div>" % (prompt, fd.getDisplayText())
					else:
						 if fd.getValue() !=None and  fd.getValue() !="":
							summary+="<div><b>%s:</b> %s</div>" % (prompt, fd.getValue())
	return summary
	
def getSupportingDocsLinks( fieldName)	:
	summary=""
	field= thisDocument .getField( fieldName)
	links=field.getDocLinks()
	if len(field.getAttachments()) :
		list = field.getAttachments()
		for file in list:
			applicationName = thisApplication.getName() # "SMS_REPORTING_1_P"
			formName= thisDocument.getFormName()
			docKey = thisDocument.getDocKey()
			keyName = "AIDMOR_VIER_ID" 		#docKey.getKeyName()
			keyValue = thisDocument.getID()
			fileName = file.getFileName()
			url = "https://airmethods.etq.com/reliance_prod/reliance?ETQ$CMD=CMD_OPEN_ATTACHMENT&ETQ$SOURCE_FIELD_NAME=%s&ETQ$APPLICATION_NAME=%s&ETQ$FORM_NAME=%s&ETQ$KEY_NAME=%s&ETQ$KEY_VALUE=%s&ETQ$PARENT_DIALOG_NAME=null&ETQ$SUBFORM_NAME=&ETQ$RECORD_ID=null&ETQ$FILE_NAME=%s&ETQ$APPLICATION_NAME=%s" % (fieldName, applicationName, formName,  keyName, keyValue, fileName,  applicationName)
			summary+="<a href='%s'  target='_blank'>%s</a></br>" % (url, fileName)
	if summary=="":
		summary="None"
	return summary
			
def clearIsEvent():
	myLog("clearIsEvent IN")
	if thisDocument.getFieldValue("I_S_EVENT_P") ==1:
		thisDocument.setFieldValue("REPORT_TYPE_5_P",None)
	myLog("clearIsEvent OUT")
	return
		
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
	myLog("clearLocationFields IN")
	locationType = thisDocument.getField("LOCATION_TYPE_2_P").getDisplayText()
	clearList =()
	if locationType =="Scene":
		clearList =(
			"EVENT_LOCATION_5_P"
			,"HOSPITAL_NAME_2_P"
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
			,"AIRPORT_NAME_P"
			,"DESCRIPTION_8_P"
			,"CITY_2_P"
			,"STATE_3_P"
		)
	if locationType =="Hospital":
		clearList = (
			"LATTITUDE_P"
			, "LONGITUDE_P"
			,"LATTITUDE_P"
			, "LONGITUDE_P"
			,"EVENT_LOCATION_5_P"
			,"AIRPORT_NAME_P"
			,"DESCRIPTION_8_P"
		)
	if locationType =="Airport":
		clearList = (
			"LATTITUDE_P"
			, "LONGITUDE_P"
			,"EVENT_LOCATION_5_P"
			,"LATTITUDE_P"
			,"EVENT_LOCATION_5_P"	
			, "LONGITUDE_P"
			,"DESCRIPTION_8_P"
		)
	if locationType =="Other":
		clearList = (
			"EVENT_LOCATION_5_P"
			,"LOCATION_IS_SECURE_1_P"
			,"HOSPITAL_NAME_2_P"
			,"EVENT_LOCATION_5_P"	
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
				,"EVENT_LOCATION_5_P"		# does this work with a pick?
				,"AIRPORT_NAME_P"
				,"DESCRIPTION_8_P"

			)	
	for fldID in clearList:
		thisDocument.setFieldValue(fldID, "")
	return
		
def gotoNextTab( ):
	myLog("gotoNextTab")
	nextTab ={	"BASIC_TAB":"EVENT_TYPE_TAB"
		,	"EVENT_TYPE_TAB":"THREAT_TAB"
		#,	"THREAT_TAB":"ERROR_TAB"
		,	"THREAT_TAB":"EVENT_DESCRIPTION_TAB"
		,	"ERROR_TAB":"EVENT_DESCRIPTION_TAB"
		,	"EVENT_DESCRIPTION_TAB":"SUMMARY_TAB"
		,	"SUMMARY_TAB":"SUMMARY_TAB" 
		,"ALL_TABS_TAB":"ALL_TABS_TAB"}	
	thisTab = thisDocument.getActiveTabDesignName()
	if thisTab !="":
		if thisTab == 	"BASIC_TAB" and 	not isEvent():
			thisDocument.gotoTab( "EVENT_DESCRIPTION_TAB")
		else:
			thisDocument.gotoTab( nextTab[thisTab])
	else:
		myLog("Hmm got no tab whats up with that?")
		return
		
	if nextTab[thisTab] == "SUMMARY_TAB":
		summary = buildSummaryQuattro() 
		thisDocument.setFieldValue("EVENT_SUMMARY_P", summary)
	return
	
def gotoPreviousTab():
	myLog("gotoPreviousTab")
	previousTab ={	"BASIC_TAB":"BASIC_TAB"
		,	"EVENT_TYPE_TAB":"BASIC_TAB"
		,	"THREAT_TAB":"EVENT_TYPE_TAB"
		,	"ERROR_TAB":"THREAT_TAB"
		#,	"EVENT_DESCRIPTION_TAB":"ERROR_TAB"
		,	"EVENT_DESCRIPTION_TAB":"THREAT_TAB"
		,	"SUMMARY_TAB":"EVENT_DESCRIPTION_TAB" 
		, 	"ALL_TABS_TAB":"SUMMARY_TAB"}	
	thisTab = thisDocument.getActiveTabDesignName()
	if thisTab !="":
		if thisTab == 	"EVENT_DESCRIPTION_TAB" and 	not isEvent():
			thisDocument.gotoTab( "BASIC_TAB")
		else:
			thisDocument.gotoTab( previousTab[thisTab])
	else:
		myLog("Hmm got no tab whats up with that?")
	return
		

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
						#"EVENT":("EVENT_TYPE_2_P","CATEGORY_2_P","QUERY_P","SUB_CATEGORY_2_P","OTHER_10_P","CATEGORY_OTHER_1_P")
	for key,value  in dictSubformAttributes.iteritems():	# instantiated in onOpen 
		loadCategorySubform(key,value[0],value[2]) #subformID and query string
	myLog("buildAllTypeLists OUT")
	return

def  getCategoryTypesAsText( sfID, catID):
	myLog( "getCategoryTypesAsText IN")
	categoryText =""
	subform = thisDocument.getSubform(  sfID)  
	if subform != None:
		for record in subform.getRecords():
			fld = record.getField(  catID )
			if fld != None:
				category = fld .getDisplayText()
				debug= "CAT %s" % category
				#myLog(debug)
				if  category != None and category != "":
					if categoryText != "":
						categoryText +=", "
					categoryText += category
			else:
				myLog( "FAILED to get CATEGORY field")

			debug = "categoryText is %s" % categoryText
			#myLog(debug)
	else:
		myLog( "FAILED to get subform")
	if categoryText =="":
		categoryText = "None selected"
	#myLog( categoryText)
	myLog( "getCategoryTypesAsText OUT ")
	return categoryText
	
	
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
	if thisDocument.getFieldValue("I_S_EVENT_P") == 1:
		return True
	return False
	
def isNotEvent():
	if thisDocument.getFieldValue("I_S_EVENT_P") == 0:
		return True
	return False	
def isHazard():
	if thisDocument.getFieldValue("I_S_EVENT_P") == 1:
		return True
	return False
def isSystemImprovement():
	if thisDocument.getFieldValue("I_S_EVENT_P") == 2:
		return True
	return False
	

conditionalHeader= {
	"FLIGHT_INFO_ID":"<h3>Flight Information</h3>"
	,"PREVENT_ID":"<h3>Prevenative Measures</h3>"
	,"SUPPORT_ID":"<h3>Attachments</h3>"
	,"EVENT_DESC_ID":"<h3>Event Description</h3>"
	,"BRIEF_EVENT_DESCRIPTION_P":"<b>Description:</b>"
	,"PREVENATIVE_MEASURES_P":""
	,"EVENT_DESCRIPTION_4_P":""
	,"EMAIL_2_P":""
	,"CONTACT_NUMBER_5_P":""
	,"EMPLOYEE_4_P":""
}	
conditionalHeaderFields= {
	"FLIGHT_INFO_ID":["I_S_EVENT_P"]
	,"PREVENT_ID":["PREVENATIVE_MEASURES_P"]
	,"SUPPORT_ID":["SUPPORTING_DOCUMENTS_9_P"]
	,"EVENT_DESC_ID":["EVENT_DESCRIPTION_4_P"]
}	
	
def submitForm():
	myLog("submitForm IN")
	debug=""
	eMailsLst = []
	UsersIDs =[]    
	purgeEmptyRecords()
	thisDocument.save()
	summary = buildSummaryQuattro()
	myLog(summary)
	thisDocument.setFieldValue("EVENT_SUMMARY_P", summary)
	officialPurposes= """
	<table class='summary'><tr><td>
	<p class = "official"  style='text-align:left'></br>Help Link: <a href='https://airport.airmethods.com/sites/Safety/etq/default.aspx'>ETQ Flightdeck Page</a></p>
	<p class="official""></br><b>Official Use Only</b></br>This report and any files or text attached to it are intended only for official	use by Air Methods Corporation and may not be transmitted, copied or
			otherwise disclosed to parties outside of Air Methods Corporation without specific authorization by an Air Methods Corporation Division President or 	their designee.</p>
	</td></tr></table>
	"""
	summary+="<p class='normal'>Click here to launch ETQ and open the AIDMOR report: "
	summary+=buildDocumentURL()
	summary+="</p>"
	
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
	loc = loc.split(':')		# Get the ending
	loc = loc[  len(loc) - 1 ]
	
	id = thisDocument.getFieldValue("ETQ$NUMBER") 	#getID()
	sfID =dictSubformAttributes["EVENT"][0]
	catID =dictSubformAttributes["EVENT"][1]
	catText =""
	catText = getCategoryTypesAsText( sfID, catID   )
	if catText=="":
		catText="--"
	reportType = ""
	if thisDocument.getField( "I_S_EVENT_P") ==  1:
		reportType = "Event - "
	else:
		if thisDocument.getField( "REPORT_TYPE_4_P") == 1:
			reportType = "Hazzard / Risk Item Report"
		if thisDocument.getField( "REPORT_TYPE_4_P") == 2:
			reportType = "System Improvement Report"

	aircraft = " | %s" % thisDocument.getField("AIRCRAFT_3_P").getDisplayText()

	subject = 'TEST AIDMOR %s | %s %s | %s %s'  % (id, reportType,catText, loc, aircraft  )  
	mailObj.setSubject(subject)  # AIDMOR 000000 Loc: Lone Tree
	mailObj.setBody(summary)
	mailObj.setSenderUserID(Rstring.toInteger(thisUser.getID()))
	mailObj.setSenderEmail(thisUser.getEmail())
	
	phase = thisDocument.getPhase()	
	dateDue = Rdate.currentDateTime()
	dateDue = Rdate.addDays( dateDue, 7)
	phase.route("SUBMITTED_1_P", dateDue, UsersIDs, [], "AIDMOR Submit",1  )
		# send the email after the document is routed successfully
	PublicMailSender.sendEmail(mailObj)
	thisDocument.close()
	thisAction.goToLastAccessedTab() 
	myLog("submitForm OUT")
	return
	


def isNoEventTypeNeeded():
	myLog("isNoEventTypeSelected IN")
	str=""
		# (SubformID, category, query string, subcategory, other)
	if isEvent():
		attributes = dictSubformAttributes["EVENT"]
		subform = thisDocument.getSubform(attributes[0])
		if subform!=None:
			for record in subform.getRecords():
				if record.getFieldValue( attributes[1]) >0:
					myLog("have an event type. isNoEventTypeNeeded OUT")
					return True
			
		myLog("NO  event type found. RETURNING FALSE  isNoEventTypeNeeded OUT ")
		return False
		
	myLog("NO event type was needed.  isNoEventTypeNeeded OUT.")
	return True
		
def validateBeforeSubmit():
	validationDict = {
		"LOCATION_TYPE_2_P":[ "HIDE_LOCATION_TYPE_P", "The location type field needs to be populated."]
		,"DESCRIPTION_8_P" :["HIDE_DESCRIPTION_2_P", "The location's description is required."]
		,"HOSPITAL_NAME_2_P":["HIDE_HOSPITAL_2_P","The hospital name needs to be identified."]
		,"AIRPORT_NAME_P":["HIDE_AIRPORT_2_P","The airport name needs to be identified."]
		,"EVENT_LOCATION_5_P":["HIDE_LOCATION_P","An event location must be selected."]
		,"CITY_2_P":["HIDE_COMMON_2_P","The city location must be entered ."]
		,"STATE_3_P":["HIDE_COMMON_2_P","The state location must be entered ."]
		,"BRIEF_EVENT_DESCRIPTION_P":["EVENT_DESCRIPTION_4_P","Please briefly describe the event/issue."]
	}
	validationWarning=""
	if thisPhase.isSendingForward():
		for fieldID, value in validationDict.iteritems():
			section = thisDocument.getSection(value[0])
			if section!=None and section.isEditable()  and thisDocument.getField(fieldID).isEmpty():
				thisDocument.getField(fieldID).addError(value[1])
				validationWarning +="\n%s" % value[1]
		if isNoEventTypeNeeded()  == False:
			validationWarning +="\nAt least one event type must be selected."
			
		if validationWarning!="":
			buildAllTypeLists()	# need to rebuild the list if not moving forward
			thisDocument.gotoTab( "ALL_TABS_TAB")
			raise ValidationException, validationWarning
	return
	
#####
def buildSummaryQuattro():	
	myLog("buildSummaryQuattro IN")
	summary = """
	<!DOCTYPE html>	<html lang="en">		<meta charset="utf-8">
	<meta name="description" content="AIDMOR event form created and sent from AirMethods ETQ Reliance">
		<head><style>
		   body.summary{   font-family: Arial;   font-size: 100%;	width:480px;	}
		   table.summary{   font-family: Arial;   font-size: 100%;   	width:480px;	border-spacing: 0px;	border-collapse: collapse;		   }
			td.summary {	font: 11px, Arial, sans-serif;	padding:0px;	text-align: left; border: ;}
			th.summary {	font: 11px, Arial, sans-serif;	padding:0px;	 }
			p.normal{ font-family: Arial;	FONT-SIZE: 8pt;;	width:480px;	text-align:left;	}
			p.official{ font-family: Arial;	font-size: 60%;	width:480px;	text-align:center;	}
			p.test{	font-family: Arial;	font-size: 120%;	width:480px;	color: red; 	text-align:center;	}
			a.AIDMOR{	font-family: Arial;   font-size: 80%;	}
			h3 {	background-color:#E0F2F7; 	}
			ul.cat { 	list-style-type: square;			}
			ul.sub {	margin-top:0;margin-bottom:0; list-style-type: disc;	list-style-position: inside;}
			div.cat {	margin: 0;}
			div.sub {	text-indent:50px; 	margin: 0; }
	</style>	<head>	<body class='summary'>	<title>AIDMOR Report Summary</title>
	<table  class='summary'><tr style="background-color:#084B8A">
	<td><font   size="4" color="white">AIDMOR Summary Report</font>
	<img src="http://www.airmethods.com/images/default-source/Defenders-Of-Tomorrow/am-logo-defenders-of-tomorrow.png?sfvrsn=6" align="right">
	</td></tr>
	<tr><td><p class="test">TEST AIDMOR</p></td>	</tr>
	</table>
	<table  class='summary' >
	"""

	headerInfo =[
		[{"<h3>Summary</h3>":2}]
		 ,[{"ETQ$NUMBER":0} ,  {"SUBMIT_DATE_2_P":6}]
		,[{"&nbsp;":2}]
		,[{"EVENT_TIME_2_P":6}]
		,[{"BRIEF_EVENT_DESCRIPTION_P":7}]
		,[{"&nbsp;":2}]
		,[{"LOCATION_TYPE_2_P":1} ]
		,[{"EVENT_LOCATION_5_P":1}	 ]
		,[{"HOSPITAL_NAME_2_P":0}	 ]
		,[{"AIRPORT_ID_P":0}	,{"AIRPORT_NAME_P":0}	 ]
		,[{"DESCRIPTION_8_P":0} ]
		,[{"CITY_2_P":0}	 , {"STATE_3_P":1} ]
		,[{"EVENT":4}]
		,[{"<h3>Submitted By:</h3>":2}]
		,[{"EMPLOYEE_4_P":13} , {"CONTACT_NUMBER_5_P":7}	  ]
		,[ {"EMAIL_2_P":7}]
		,[{"ETQ$LOCATIONS":1} ]
		,[{"<h3>Event / Hazard Location</h3>":2}]
		,[{"LOCATION_TYPE_2_P":1}  ]
		,[{"DESCRIPTION_8_P":0} ]
		,[{"EVENT_LOCATION_5_P":1}	 ]
		,[{"HOSPITAL_NAME_2_P":0}	 ]
		,[{"AIRPORT_ID_P":0}	,{"AIRPORT_NAME_P":0}	 ]
		,[{"CITY_2_P":0}	 ,  {"STATE_3_P":1} ]
		,[ {"LATTITUDE_P":0}	 ,  {"LONGITUDE_P":0}]
		,[{"LOCATION_OWNER_S_NAME_P":0}		, {"LOCATION_OWNER_NUMBER_P":0}		]
		,[{"LOCATION_IS_SECURE_1_P":1}	 ]		
		,[{"FLIGHT_INFO_ID":5}]
		,[{"EVENT_TIME_2_P":6},{"EVENT_TIME_3_P":9} ]
		,[{"AIRCRAFT_3_P":8} ,{"AIRCRAFT_3_P":11}	]  
		,[{"AIRCRAFT_3_P":12}]
		,[{"FLIGHT_TYPE_2_P":1},{"FLIGHT_NUMBER_2_P":0} ]
		,[{"EVENT_PHASE_TYPE_MX_2_P":1}	,{"EVENT_PHASE_TYPE_OPS_1_P":1}]		
		,[{"PATIENT_ON_BOARD_P":1}, {"PRESSURE_TO_FLY_P":1} ]
		,[ {"&nbsp;":2}]
		,[ {"DAY_NIGHT_3_P":1}, {"NVG_3_P":1},	 ]   
		,[ {"CONDITIONS_P":1}, {"WEATHER_AS_FORECAST_P":1}]
		,[{"CEILING_AGL_P":0}	, {"VISIBILITY_SM_P":0}  	]
		,[ {"&nbsp;":2}]
		,[{"TIME_IN_AIRCRAFT_P":0},  {"FLOWN_LAST_30_P":0}	]
		,[ {"PILOT_TOTAL_TIME_P":0}, {"FLOWN_LAST_90_P":0}	  ]
		,[{"<h3>Event / Report Description</h3>":2}]
		,[{"EVENT_DESCRIPTION_4_P":7} ]
		,[{"PREVENT_ID":5}]
		,[{"PREVENATIVE_MEASURES_P":10} ]
		,[{"SUPPORT_ID":5}]
		,[{"SUPPORTING_DOCUMENTS_9_P":3} ]
		]
		
	for rows in headerInfo:
		dataList=[]
		for column in rows:
			data = slurpField2( column)
			if len(data)>0:
				dataList.append( data)
		if len(dataList)>0:		
					# define how many columns are in use
			summary+="<tr><td><table  class='summary'  ><tr>"
			for i in range(1,len(dataList)):
				summary+="<th class='summary' width='%s%%'></th>" % str(100/len(dataList))
			summary+="</tr>\n<tr>"
			for data in dataList:
				summary+="<td class='summary' >%s</td>\n" % ( data)
			summary+="</tr>\n</table></td></tr>\n"
	summary+="</table></body></html>"		
	myLog("buildSummaryQuattro IN")
	return summary
		

def slurpField2( dict):
	myLog("slurpField2 IN")
	displayType=["Plain Text", "Pick List", "Header","Attachments","SubForm","Conditional Header","Special Date","Replacement Prompt"]
	content = ""
	for key, value in dict.items():
		str = "key %s value %s" % (key, value)
		#myLog(str)
		if value in (0,1,6,7,8,9,11,12):
			fd=thisDocument.getField(key)
			if  fd  == None or fd.getValue() == None or fd.getValue() =="":	# nothing here to fetch
				#content=" "	#placeholder &nbsp;
				myLog("slurpField2 OUT")
				return content
			
		if value ==0: # string value
			prompt = fd.getPrompt()
			content+="<b>%s</b> %s" % (prompt, fd.getValue())
		elif value == 1: # pick list
			prompt = fd.getPrompt()
			content+="<b>%s</b> %s" % (prompt, fd.getDisplayText())
		elif value == 2: # nakey HTML
			content+= key
		elif value == 3: # supporting Docs
			content+=getSupportingDocsLinks( key)
		elif value == 4:
			content += slurpSubform( dictSubformAttributes[key])
		elif value == 5:
			for fld in conditionalHeaderFields[key]:
				if thisDocument.getFieldValue(fld) !=None or thisDocument.getFieldValue(fld)!="":
					content += conditionalHeader[key]
					break		
		elif value == 6:	# special case date field just the date name' 1/22/16 9:13 MST
			prompt = fd.getPrompt()
			dt = fd.getDisplayText()
			dt = dt.split()
			content+="<b>%s </b> %s %s %s" % (prompt, dt[0], dt[1], dt[2])
		elif value == 7:	# use replacement prompt
			fd=thisDocument.getField(key)
			content+="<b>%s</b> %s" % ( conditionalHeader[key], fd.getValue())
		elif value == 13:	# use replacement prompt AND PICK
			fd=thisDocument.getField(key)
			content+="<b>%s</b> %s" % ( conditionalHeader[key], fd.getDisplayText())
		elif	value==8: 	## aircraft special case
			ac = fd.getDisplayText()
			ac = ac.split(":") #N581AM : 4438 : AS350B2
			content+="<b>Aircraft:</b> %s "%(ac[0])
		elif	value==11: 	## aircraft special case
			ac = fd.getDisplayText()
			ac = ac.split(":") 
			content+="<b>Serial #:</b> %s "%(ac[1])			
		elif	value==12: 	
			ac = fd.getDisplayText()
			ac = ac.split(":") 
			content+=" <b>Type:</b> %s"%(ac[2])			
		elif	value==9: 	## just the time  THIS IS USING THE medium FORMAT FROM etq 
			prompt = prompt=fd.getPrompt()
			dt = fd.getDisplayText()
			dt = dt.split()
			hours =dt[0].split(":")
			content+="<b>%s</b> %s:%s %s" % (prompt, hours[0],  hours[1], dt[1])		
		elif value == 10:	# use replacement prompt
			fd=thisDocument.getField(key)
			fieldText = fd.getValue()
			if fieldText==None or fieldText=="":
				fieldText="None"
			content+="<b>%s</b> %s" % ( conditionalHeader[key], fieldText)
	myLog("slurpField2 OUT")
	return content

def isPropertyDamage(  ) :
	myLog("isPropertyDamage IN") 			#"Property Damage" 	"EVENT":("EVENT_TYPE_2_P","CATEGORY_2_P","QUERY_P","SUB_CATEGORY_2_P","OTHER_10_P","CATEGORY_OTHER_1_P")
	subform = thisDocument.getSubform("EVENT_TYPE_2_P")  
	if (subform!=None) and (subform.size() >0):
		list = subform.getEncodedTextListFromAllRecords("CATEGORY_2_P", ';')
		if "Property Damage" in list:
			return  True
	return False
	
def isButtonActive(buttonID):
	myLog("isButtonActive IN")
	tabName = thisDocument.getActiveTabDesignName()
	str = "The active tabName is %s\n and the button id is %s" % (tabName, buttonID)
	myLog(str)
	if buttonID == "NEXT_6_P":
		myLog( "NEXT_6_P matched")
		str = "tabName is <%s>" % tabName
		myLog(str)
		if tabName in "SUMMARY_TAB" or tabName in  "ALL_TABS_TAB":
			myLog("is SUMMARY_TAB or ALL_TABS_TAB return FALSE")
			return False
	elif buttonID =="PREVIOUS_4_P":
		myLog( "PREVIOUS_4_P matched")
		if tabName =="BASIC_TAB":
			myLog("is BASIC_TAB RETURN TRUE")
			return False
			
	myLog("fell through returning True")
	return True

#def showLocationType():
#	return True

	
def isSubmittedPhase():
	return( thisPhase.getName()== "SUBMITTED_1_P" )	
	
def isDraftPhase():	
	return( thisPhase.getName()== "START_16_P")
	
def isSectionEditable():	
	if  isDraftPhase():
		return True
	if isSubmittedPhase():
		if  isEditable:
			return True
		return False
		
def isSectionReadOnly():
	if  isDraftPhase():
		return False
	if isSubmittedPhase():
		if  isEditable:
			return False
		return True
		
		
def getCategoryCheckBoxen2( queryField):
	debug = "getCategoryCheckBoxen2 In \n "
	debug  += "What is in the query field %s\n" % queryField

	queryValue = thisSubformRecord.getField(queryField).getDisplayText()	
	debug +="\nIt contains the display string <%s>\n" % queryValue
	
	myLog(debug)
	
	sql="""
		select  ETE.CATEGORY_6 DESCRIPTION ,  ETE.EVEN_THEREA_ERROR_ID ID, IFNULL(ETE.POSITION, 0) POS
		from external_data.event_thereat_error ETE
		left join LOOKUPS.COMPANY_1 comp on ( ETE.COMPANY_3_ID = comp.COMPANY_1_ID)
		left join LOOKUPS.ORG ORG on ( ETE.DIVISION_ID = ORG.ORG_ID)
		where  	"""
	sql = """
		SELECT
			EVENT_THEREAT_ERROR.EVEN_THEREA_ERROR_ID ID,
			EVENT_THEREAT_ERROR.CATEGORY_6 DESCRIPTION,
			EVENT_THEREAT_ERROR.SUB_CATEGORY_4 SUBCAT,
			COMPANY_1_1.DESCRIPTION COMPANY,
			DEPARTMENT.DEPARTMENT_NAME DIV_DEPART_NAME,
			EVENT_THREAT_ERROR.DESCRIPTION EVTHER_TYPE,
			BOOLEAN_VALUES.DESCRIPTION DISABLED,
			EVENT_THEREAT_ERROR.POSITION POS

		FROM EXTERNAL_DATA.EVENT_THEREAT_ERROR EVENT_THEREAT_ERROR
			LEFT JOIN ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES ON (EVENT_THEREAT_ERROR.DISABLED_ID = BOOLEAN_VALUES.VALUE )
			LEFT JOIN LOOKUPS.EVENT_THREAT_ERROR EVENT_THREAT_ERROR ON (EVENT_THEREAT_ERROR.EVENT_THREAT_ERROR_ID = EVENT_THREAT_ERROR.EVENT_THREAT_ERROR_ID )
			LEFT JOIN EXTERNAL_DATA.COMPANY COMPANY_2 ON (EVENT_THEREAT_ERROR.EVEN_THEREA_ERROR_ID = COMPANY_2.EVEN_THEREA_ERROR_ID )
			LEFT JOIN LOOKUPS.COMPANY_1 COMPANY_1_1 ON (COMPANY_2.COMPANY_ID = COMPANY_1_1.COMPANY_1_ID )
			LEFT JOIN EXTERNAL_DATA.DIVISION_DEPARTMENT DIVISION_DEPARTMENT ON (EVENT_THEREAT_ERROR.EVEN_THEREA_ERROR_ID = DIVISION_DEPARTMENT.EVEN_THEREA_ERROR_ID )
			LEFT JOIN LOOKUPS.DEPARTMENT DEPARTMENT ON (DIVISION_DEPARTMENT.DIVISION_DEPARTMENT_ID = DEPARTMENT.DEPARTMENT_ID )
			WHERE EVENT_THEREAT_ERROR.disabled_id = 0 
			
		"""		
# 			LEFT JOIN LOOKUPS.COMPANY_1 COMPANY_1 ON (EVENT_THEREAT_ERROR.COMPANY_3_ID = COMPANY_1.COMPANY_1_ID )
		
	emptySQL = 	"""
		select  EVENT_THEREAT_ERROR.CATEGORY_6 DESCRIPTION , IFNULL(EVENT_THEREAT_ERROR.POSITION, 0) POS, EVENT_THEREAT_ERROR.EVEN_THEREA_ERROR_ID ID
		from external_data.event_thereat_error EVENT_THEREAT_ERROR
		WHERE EVENT_THEREAT_ERROR.CATEGORY_6  =''
	"""
	
	if queryValue!="":
		whereClause = "AND 	COMPANY_1_1.DESCRIPTION  = '%s'  AND DEPARTMENT.DEPARTMENT_NAME = '%s' AND  EVENT_THEREAT_ERROR.CATEGORY_6 ='%s' " %( company, org, queryValue)
		sql+=whereClause
		sql+='		group by  EVENT_THEREAT_ERROR.CATEGORY_6 '
		sql+= ' ORDER BY EVENT_THEREAT_ERROR.POSITION,   EVENT_THEREAT_ERROR.CATEGORY_6  '
	
		myLog("use the GOOD SQL")
		myLog(sql)
		thisField.setQueryParameter("VAR$USER", sql)
	else:
		thisField.setQueryParameter("VAR$USER", emptySQL)
		myLog("use the EMPTY SQL")

	myLog("getCategoryCheckBoxen2 Out")
	return
	
def getAIDMORCategory( appSpace, dataSource, comp, org, evther):
	myLog("getAIDMORCategory IN")
	param = { #external_data
		"ETQ$APPLICATION":appSpace,
		"AMC$COMP":comp,
		"AMC$ORG": org,
		"AMC$EVTHER":  evther		
		}

	# dict =  makeDAOQuery(dataSource, param)
	list = makeDAOQueryList(dataSource, param)
	myLog("getAIDMORCategory OUT")

	return list	
	#######################
def buildCategoryCheckList2( mklList, parentSF,queryFieldID):
	myLog("buildCategoryCheckList2 IN")
	recordCount = 0
	debug=""
	myLog(queryFieldID)
	currentKey =""
	
	for value in mklList:
		debug =" value[DESCRIPTION] %s\n" %(value["DESCRIPTION"])
		myLog(debug)
		newKey = value["DESCRIPTION"]
			
		#debug+="currentKey: <%s>  newKey <%s> NOT EQUAL %s\n" %(newKey, currentKey,(newKey != currentKey))
		recordAlreadyExists = False
		for record in parentSF.getRecords():
			currentFieldValue = record.getFieldValue( queryFieldID)
			# debug+="***currentFieldValue: <%s>  newKey <%s> NOT EQUAL %s\n" %(currentFieldValue, currentKey,(newKey != currentFieldValue))			
			if  newKey == currentFieldValue :
				recordAlreadyExists = True
				break
				
		if recordAlreadyExists == True:
			debug += ("record already exists!\n")
		else:
			debug+="*>*>*>*>currentKey: <%s>  newKey <%s> NOT EQUAL %s\n" %(currentKey, newKey,(newKey != currentKey))			
			if  newKey != currentKey:
				recordCount +=1
				currentKey = newKey
				newRecord = parentSF.newRecord()
				newRecord.setFieldValue( queryFieldID , currentKey)
				debug+="Set queryFieldID %s to %s\n" % ( queryFieldID , currentKey)
	debug+="recordCount %s for queryFieldID %s\n" % (recordCount, queryFieldID)
	myLog(debug)
		#thisDocument.setFieldValue("DEBUG_29_P",debug)
	myLog("buildCategoryCheckList2 OUT")
	return
	
def getSubCategoryCheckBoxen2( cat, queryField):
	debug = "getSubCategoryCheckBoxen2 In - %s " % queryField
	myLog(debug)
	queryValue = thisSubformRecord.getField( queryField).getValue()
	if queryValue!=None:
		sql=	"""
			SELECT  ETE.SUB_CATEGORY_4 DESCRIPTION, ETE.POSITION POS, ETE.EVEN_THEREA_ERROR_ID ID
			FROM  external_data.event_thereat_error ETE
			LEFT JOIN  LOOKUPS.COMPANY_1 comp on ( ETE.COMPANY_3_ID = comp.COMPANY_1_ID)
			LEFT JOIN  LOOKUPS.ORG ORG on ( ETE.DIVISION_ID = ORG.ORG_ID)
			LEFT JOIN  LOOKUPS.event_threat_error EVTHER on (ETE.EVENT_THREAT_ERROR_ID =EVTHER.EVENT_THREAT_ERROR_ID)
			WHERE ETE.disabled_id = 0 	
			"""
		sql=	"""
		SELECT
			EVENT_THEREAT_ERROR.EVEN_THEREA_ERROR_ID ID,
			EVENT_THEREAT_ERROR.CATEGORY_6 CAT,
			EVENT_THEREAT_ERROR.SUB_CATEGORY_4 DESCRIPTION,
			COMPANY_1_1.DESCRIPTION COMPANY,
			DEPARTMENT.DEPARTMENT_NAME DIV_DEPART_NAME,
			EVENT_THREAT_ERROR.DESCRIPTION EVTHER_TYPE,
			BOOLEAN_VALUES.DESCRIPTION DISABLED,
			EVENT_THEREAT_ERROR.POSITION POS

		FROM EXTERNAL_DATA.EVENT_THEREAT_ERROR EVENT_THEREAT_ERROR
			LEFT JOIN ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES ON (EVENT_THEREAT_ERROR.DISABLED_ID = BOOLEAN_VALUES.VALUE )
			LEFT JOIN LOOKUPS.EVENT_THREAT_ERROR EVENT_THREAT_ERROR ON (EVENT_THEREAT_ERROR.EVENT_THREAT_ERROR_ID = EVENT_THREAT_ERROR.EVENT_THREAT_ERROR_ID )
			LEFT JOIN EXTERNAL_DATA.COMPANY COMPANY_2 ON (EVENT_THEREAT_ERROR.EVEN_THEREA_ERROR_ID = COMPANY_2.EVEN_THEREA_ERROR_ID )
			LEFT JOIN LOOKUPS.COMPANY_1 COMPANY_1_1 ON (COMPANY_2.COMPANY_ID = COMPANY_1_1.COMPANY_1_ID )
			LEFT JOIN EXTERNAL_DATA.DIVISION_DEPARTMENT DIVISION_DEPARTMENT ON (EVENT_THEREAT_ERROR.EVEN_THEREA_ERROR_ID = DIVISION_DEPARTMENT.EVEN_THEREA_ERROR_ID )
			LEFT JOIN LOOKUPS.DEPARTMENT DEPARTMENT ON (DIVISION_DEPARTMENT.DIVISION_DEPARTMENT_ID = DEPARTMENT.DEPARTMENT_ID )
			WHERE EVENT_THEREAT_ERROR.disabled_id = 0 

			"""			
		whereClause = "AND EVENT_THREAT_ERROR.DESCRIPTION ='%s' AND COMPANY_1_1.description = '%s' AND DEPARTMENT.DEPARTMENT_NAME = '%s' AND  EVENT_THEREAT_ERROR.CATEGORY_6 = '%s' " % (cat, company, org,queryValue)
		sql+=whereClause+"  ORDER BY EVENT_THEREAT_ERROR.POSITION, EVENT_THEREAT_ERROR.SUB_CATEGORY_4  "
		myLog("XXXXXX")
		myLog(sql)
		thisField.setQueryParameter("VAR$USER", sql)

	myLog("getSubCategoryCheckBoxen2 Out")
	return
	
	