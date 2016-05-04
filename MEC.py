from com.etq.util import Log
chatty=True

def myLog( message):
	if chatty:
		Log.info("",message)
	return
	
def getAircraftListQuery( ):
	debug = "getAircraftListQuery In " 
	myLog(debug)
	sql=	"""
			SELECT  CONCAT ( AIRCRAFT. SERIAL , " : ", AIRCRAFT. REGISTRATION,  " : ", AIRCRAFT.TYPE )   			DESCRIPTION
			,  AIRCRAFT.ACRAFT2_ID ID
			FROM  external_data.ACRAFT2 AIRCRAFT
			WHERE AIRCRAFT.disabled = 0 	
			AND AIRCRAFT.FLEET_ID= 1
			ORDER BY AIRCRAFT.REGISTRATION
			"""
	myLog(sql)
	thisField.setQueryParameter("VAR$USER", sql)

	myLog("getAircraftListQuery Out")
	return
	
def createMEC():
	debug =""
	if thisDocument.save():
		parentID = thisDocument.getID()

		newMec = thisApplication.newDocument( "MCS_P", "START")

		# , parentID, "ETQ$SOURCE_LINK")
		if newMec:
			debug+="newMec is something\n"
		else:
			debug+="newMec failed\n"
		fields ={
			#"AIRCRAFT_D":"AIRCRAFT_ID_3_P", 	AIRCRAFT_3_P
			"AIRCRAFT_D":"AIRCRAFT_3_P", 	
			"REGION_3_P":"REGION_2_P", 	
			"OOS_DT_P":"OOS_DATE_TIME_1_P", 	
			"MOC_P":"MOC_REQUIRED_P", 	
			"LOG_P":"LOGBOOK_ENTRY_COMPLETE_P",
			"EST_RTS_P":"REVISED_RTS_P", 	
			"MECHANIC_NAMESS_P":"PRIMARY_MX_2_P", 	
			"TIER_STATUS_1_P":"TIER_2_STATUS_P",
			"FIELD_411_IN_P":"OOS_IN_411_P", 	
			"LATE_START_3_P":"REASON_P",
			"REASON_OOS_P":"OPEN_CLOSED_NOTES_P",
			"REASON_OOS_1_P":"OOS_REASON_P" } 

		# what the heck 	
		# since the field types dont match between the forms use the the reset value as base of index to the new value
		reset ={	"MOC_P":[2,1], 	"LOG_P":[2,1],	"FIELD_411_IN_P":[2,1]		}
		for fieldLog, fieldMEC in fields.iteritems():
			value = thisDocument.getFieldValue(fieldLog)
				#check =boxen use 0,1 for no yes and radio buttons range 1-n
			if  fieldLog in reset :
				value = reset[fieldLog][value]
				
			newMec.setFieldValue( fieldMEC, value)
			debug+= "%s: %s  %s\n" % (fieldLog, fieldMEC, value)
		base = thisDocument.getField("BASE_D") .getDisplayText()
		if len(base) >1:
			base = base.split(':')[2]
			newMec.setFieldValue("BASE_LOCATION_P",  base)	# do this special translate from list item to text
				
		
		# ACCOUNT FOR LATE START	and set the RB value copied above
		oosDT = thisDocument.getField("OOS_DT_P").getDisplayText()
		bits = oosDT.split(" ")
		oosTime = bits[3].split(":")
		if  int(oosTime[0] )>5 and thisDocument.getFieldValue("SCHEDULED_P" ) == 1:
			newMec.setFieldValue( "LATE_START_P", 1)

			
		aidmorId = thisDocument.getFieldValue("AIDMOR_2_P")
		if aidmorId == None or aidmorId =="":
			debug+="Skip the aidmor record\n"
		else:
			subform = newMec.getSubform("INCIDENT_P")
			record = subform.newRecord()
			record.setFieldValue("INCIDENT_ID_P", aidmorId)
			record.setFieldValue("REPORT_TYPE_P", 1)
			debug+="<%s> aidmorId\n" % aidmorId
			
		newMec.setFieldValue("MX_RELEASE_P", makeUMRN())

				# link the two docs together
		if thisDocument.save():
			links = newMec.getField("ETQ$TARGET_LINK")
			docLink = PublicDocLink.createDocLink( thisApplication.getName(), "MCAS_CALL_LOG_P", Rstring.toInteger(thisDocument.getID()))
			if links !=None:
					links.addDocLink(docLink)
			thisDocument.save()
				
		if newMec.save():
				# after save the document I should have a doc id that i can work with
			docLink = PublicDocLink.createDocLink( thisApplication.getName(), "MCS_P", Rstring.toInteger(newMec.getID()))
			links = thisDocument.getField("ETQ$TARGET_LINK")
			if links !=None:
				links.addDocLink(docLink)
			newMec.save()			# save it again to pick up the link
			#newMec.close()	
			
			# phase shift
			logPhase = thisDocument.getPhase()
			logPhase.route("CLOSED_2_P", 1)	
			thisDocument.save()
			thisDocument.close()
			thisAction.goToLastAccessedTab() 
	else:
				debug+="Could not save the call log entry\n"
	#thisDocument.getField("DEBUG_15_P").setValue(debug)

	return
	
def makeUMRN():
	debug=""
		# this bit of code was stolen mec refresh then modified to use log fields 	
	date = thisDocument.getField("OOS_DT_P").getValue()
	date = thisDocument.getField("OOS_DT_P").getDisplayText()
	user = thisUser.getDisplayName()
	userLast = thisUser.getLastName()
	userFirst =thisUser.getFirstName()
	# tailID = thisDocument.getFieldValue("AIRCRAFT_NO_P") # TAIL_NUMBER_P
	tailID = thisDocument.getField("AIRCRAFT_D").getDisplayText() # TAIL_NUMBER_P
	tailID = tailID.split(':')	#normalize the serial number since we are now using a composite 
	tailID=tailID[0]
	tailID=tailID.strip()
	debug+="tailID is %s\n" % tailID
	
	month = {"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
	user = user.split(" ")
	dateTime = str(date).split(" ")    # Mar, 5,, 2015, 11:31:00, AM
	dd = dateTime[1].split(',')
	time =dateTime[3].split(":")
	formattedDate = "%02d%02d%c%c" % ( month[dateTime[0]], int(dd[0]),  dateTime[2][2], dateTime[2][3])
	umrn = "%s.%s.%02d%02d.%c%c" %( tailID ,formattedDate, int(time[0]),int(time[1]), userFirst[0], userLast[0] )
	return umrn
	
def createAVT():
	debug =""
	if thisDocument.save():
		parentID = thisDocument.getID()
		newAVT = thisApplication.newDocument( "AVT_P", "START")
		
		base = thisDocument.getField("BASE_D").getDisplayText() .split(":")
		region=base[0]
		debug+=region
		newAVT.setFieldValue( "REGION_D",  region )
		newAVT.setFieldValue( "BASE_1_D", base[2])
		newAVT.setFieldValue( "PROGRAM_D", base[1])
		newAVT.setFieldValue( "AIRCRAFT_4_P", thisDocument.getField("AIRCRAFT_D").getDisplayText() )
		newAVT.setFieldValue("TAIL_NUMBER_D", makeUMRN() )
		newAVT.setFieldValue("CONTACT_MECHANIC_D", thisDocument.getField("MECHANIC_NAMESS_P").getDisplayText() )
		newAVT.setFieldValue("INITIAL_DESCRIPTION_P", thisDocument.getField("REASON_OOS_1_P").getDisplayText() )
		newAVT.setFieldValue("DATE_5_P", thisDocument.getField("OOS_DT_P").getDisplayText() )
		Rutilities.debug(thisDocument.getField("OOS_DT_P").getDisplayText())
		
		if newAVT.save():
			docLink = PublicDocLink.createDocLink( thisApplication.getName(), "AVT_P", Rstring.toInteger(newAVT.getID()))
			links = thisDocument.getField("ETQ$TARGET_LINK")
			if links !=None:
				links.addDocLink(docLink)

			docLink = PublicDocLink.createDocLink( thisApplication.getName(), "MCAS_CALL_LOG_P", Rstring.toInteger(thisDocument.getID()))
			links = newAVT.getField("ETQ$SOURCE_LINK")
			if links !=None:
				links.addDocLink(docLink)
			newAVT.save()			# save it again to pick up the link
			
			# phase shift
			logPhase = thisDocument.getPhase()
			logPhase.route("CLOSED_2_P", 1)	
			thisDocument.save()
			thisDocument.close()
			thisAction.goToLastAccessedTab() 
	#thisDocument.getField("DEBUG_15_P").setValue(debug)
	return