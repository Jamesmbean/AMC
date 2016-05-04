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

def  makeDAOQuery( datasourceName, param):
	dao = thisApplication.executeQueryFromDatasource( datasourceName, param) # "MKL_LOOKUP_P"
	dict={}
	debug= "dao.count: %s\n" % dao.count()
	debug+="%s\n" % param
	while dao.next():		## next will start at the first entry and iterate through
		dict[dao.getValue("ID")] = dao.getValue("DESCRIPTION")
		debug+="key:%s val:%s\n" % (dao.getValue("ID"),dao.getValue("DESCRIPTION"))
	debug+= "dict: %s\n" % dict	
	myLog(debug)
	return dict	

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
	
def slurpFieldList( fieldList):
	summary = ""
	for li in fieldList:
		for field, displayText in li.iteritems():
			fd = thisDocument.getField(field)
			if displayText==1:
				if fd.getValue() !=None:
					summary+="<div><b>%s:</b> %s</div>" % (fd.getPrompt(), fd.getDisplayText())
			else:
				 if fd.getValue() !=None and  fd.getValue() !="":
					summary+="<div><b>%s:</b> %s</div>" % (fd.getPrompt(), fd.getValue())
	return summary	
	
def buildSummary():	
	headerInfo =(
			 {"ETQ$NUMBER":0}
			 ,{"NONEMPLOYEE_P":1}
			 ,{"OTHER_DESCRIPTION_P":0}
			 ,{"BOOKING_AGENCY_P":0}
			 ,{"HOTEL_1_P":0}
			 ,{"NAME_P":0}
			 ,{"NIAR_DATE_P":0}
			 ,{"ADDRESS_P":0}
			 ,{"CITY_4_P":0}
			 ,{"STATE_5_P":1}
			 ,{"ZIP_P":0}
			 ,{"COUNTRY_P":0}
			 ,{"PHONE_1_P":0}
			 ,{"EMAIL_3_P":0}
			 ,{"INJURY_ILLNESS_P":0}
			 ,{"PROPERTY_DAMAGE_P":0}
			 ,{"INCIDENR_DESCRIPTION_P":0}
			 ,{"PILOT_2_P":1}
			 ,{"FIRST_AID_PROVIDED_P":1}
			 ,{"MEDIC_P":0}
			 ,{"EMS_CALLED_P":1}
			 ,{"FIRE_CALLED_P":1}
			 ,{"POLICE_CALLED_P":1}
			 ,{"SENT_HOSPITAL_P":1}
			 ,{"HOSPITAL_NAME_3_P":0}
			 ,{"TRANSPORTATION_P":1}
			 ,{"EMPLOYEE_WITNESS_P":0}
			 ,{"EMPLOYEE_WITNESS_PHONE_P":0}
			 ,{"DEPARTMENT_11_P":0}
			 ,{"NON_EMPLOYEE_WITNESS_P":1}
			 ,{"NONEEMPLOYEE_PHONE_P":0}
			 ,{"NE_WITNESS_ADDRESS_P":0}
			 ,{"SUBMITTED_BY_5_P":0}
	)
	
	#http://www.sundancehelicopters.com/wp-content/themes/bootstrap-basic/img/logo.png
	#http://www.sundancehelicopters.com/wp-content/themes/bootstrap-basic/img/heli/heli2.png
	
	summary='<!DOCTYPE html><html><body style="background-color:#E5E4E2"><table style="width:100%"><tr ><td><font  face="arial" size="5" color="#FFA62F">Non-employee Incident Accident Report</font>'
	summary+='<img src="http://www.sundancehelicopters.com/wp-content/themes/bootstrap-basic/img/heli/heli2.png" align="right" height="150px">'
	summary+='</td></tr></table>'
	summary += slurpFieldList( headerInfo)
	summary+="</body></html>"
	thisDocument.setFieldValue("SUMMARY_8_P", summary)

def submitForm():
	debug=""
	eMailsLst = []
	UsersIDs =[]    
	thisDocument.save()
	buildSummary()
	summary = thisDocument.getField("SUMMARY_8_P").getValue()
	StrUsersIDs = userManager.convertToUsers(["NIAR_REPORT_P"])	

	for usersID in StrUsersIDs:
		 email = eccProfileManager.getUserProfile(Rstring.toInteger(usersID)).getEmail()
		 eMailsLst.append(email)
		 UsersIDs.append(Rstring.toInteger(usersID))
	  
	eMailsLst.append( thisUser.getEmail())
	mailObj = PublicMail()
	mailObj.setToEmails(eMailsLst)
	mailObj.setToUserIDs(UsersIDs)
	nemp = thisDocument.getField("NONEMPLOYEE_P").getDisplayText() 
	id = thisDocument.getID()
	subject = 'NIAR %s : %s'  % (id, nemp)
	mailObj.setSubject(subject)  
	mailObj.setBody(summary)
	mailObj.setPublicDocument(thisDocument)
	mailObj.setSenderUserID(Rstring.toInteger(thisUser.getID()))
	mailObj.setSenderEmail(thisUser.getEmail())
	PublicMailSender.sendEmail(mailObj)
	id =int( thisUser.getID())
	dateDue = Rdate.currentDateTime ()

	thisDocument.close()
#	thisAction.goToLastAccessedTab() 
	