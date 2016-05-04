headerInfo =(
		 {"ETQ$NUMBER":0}
		 ,{"EVENT_TIME_2_P":0}
)

conditionFields = ( 	
		{"EVENT_TIME_2_P":0}	
		,{"EVENT_PHASE_TYPE_MX_2_P":1}			
		,{"EVENT_PHASE_TYPE_OPS_1_P":1}		
		,{"AIRCRAFT_3_P":1}
		,{"FLIGHT_TYPE_2_P":1}	
		,{"FLIGHT_NUMBER_2_P":0}	
		,{"PATIENT_ON_BOARD_P":1}
		,{"CONDITIONS_P":0}	
		,{"DAY_NIGHT_3_P":1}	
		,{"NVG_2_P":1}	
		,{"WEATHER_AS_FORECAST_P":1}
		,{"CEILING_AGL_P":0}
		,{"VISIBILITY_SM_P":0}
		,{"TIME_IN_AIRCRAFT_P":0}
		,{"FLOWN_LAST_30_P":0}
		,{"FLOWN_LAST_90_P":0}
		,{"PILOT_TOTAL_TIME_P":0}
		)
submitterFields  = (	
		{"SUBMITTED_BY_4_P":0}
		,{"EMPLOYEE_4_P":1}	
		,{"CONTACT_NUMBER_5_P":0}	
		,{"EMAIL_2_P":0}	
		,{"SUBMIT_DATE_2_P":0}
		,{"ETQ$LOCATIONS":1}
		,{"COMPANY_2_P":1}
		,{"ORG_2_P":1}
		,{"BRIEF_EVENT_DESCRIPTION_P":0}
		)
locationFields = (	
		{"LOCATION_TYPE_2_P":1}	
		, {"DESCRIPTION_8_P":0} 
		 ,{"CITY_2_P":0}
		 ,{"STATE_3_P":1}
		 ,{"LATTITUDE_P":0}	 
		, {"LONGITUDE_P":0} 
		,{"LOCATION_OWNER_S_NAME_P":0}
		,{"LOCATION_OWNER_NUMBER_P":0}		
		,{"LOCATION_IS_SECURE_1_P":1}	
		,{"AMC_BASE_1_P":0}
		,{"EVENT_LOCATION_5_P":1}	
		,{"HOSPITAL_NAME_2_P":0}	
		,{"AIRPORT_ID_P":0}	
		,{"AIRPORT_NAME_P":0}	
		)
catList = (		 {"Event Location":locationFields}		, {"Submitter Information":submitterFields}	,{"Event /Flight Information":conditionFields} )	
	
def buildSummary():
	myLog("buildSummary Start")
	summary='<table style="width:100%"><tr style="background-color:#084B8A"><td><font  face="arial" size="6" color="white">AIDMOR Summary Report</font>'
	summary+='<img src="http://www.airmethods.com/images/default-source/Defenders-Of-Tomorrow/am-logo-defenders-of-tomorrow.png?sfvrsn=6" align="right">'
	summary+='</td></tr></table>' ##<h2>AIDMOR Summary:</h2>'
		
		## the second element of the dict changes how to wuery the value or the text portion from a list
	eventDescription =(		# this is not currently used but probably should be
		{"EVENT_DESCRIPTION_4_P":0}			
		,{"PREVENATIVE_MEASURES_P":0}		
	)
	
		## CREATE A LIST THAT CAN BE ITERATED IN ORDER
	summary+= slurpFieldList( {"AIDMOR":headerInfo})
	summary+= slurpSubform( dictSubformAttributes["EVENT"])
	summary+="</br>"
	for fieldList in catList:
		summary+= slurpFieldList( fieldList)
							
	for cat in ("THREAT", "ERROR"):
		summary+=slurpSubform(dictSubformAttributes[cat]	) # instantiated in onOpen 
				
	str = thisDocument.getFieldValue("EVENT_DESCRIPTION_4_P")
	if len(str)>0:
		summary+="<p><b>Event Description:</b> %s</p>" %  str
	str= thisDocument.getFieldValue("PREVENATIVE_MEASURES_P")
	if len(str)>0:
		summary+="<p><b>Prevenative Measure:</b> %s</p>" %  str
	
	fieldName = "SUPPORTING_DOCUMENTS_9_P"
	field= thisDocument .getField( fieldName)
	links=field.getDocLinks()
	if len(field.getAttachments()) :
		summary+="<h2>Supporting Documents:</h2>"
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
			thisDocument.setFieldValue("TEST_P", url)
			thisDocument.setFieldValue("TEST_NAME_P", fileName)

	thisDocument.setFieldValue("EVENT_SUMMARY_P", summary) 
	myLog("buildSummary Finish")
	return

###### buildSummary() ##############	


def buildSummaryToo():
	myLog("buildSummaryToo Start")
	summary = """
	<!DOCTYPE html>	<html lang="en">		<meta charset="utf-8">
	<meta name="description" content="AIDMOR event form created and sent from Airmethods ETQ Reliance">
	<meta name="keywords" content="Accident Incident Damage">
		<head><style>
		   body.summary{
		   font-family: Arial;
		   font-size: 100%;
			width:480px;
			}
		   table.summary{
		   font-family: Arial;
		   font-size: 100%;
		   	width:480px;					 
		    }
			p.official{
			font-family: Arial;
			font-size: 60%;
			}
			p.test{
			font-family: Arial;
			font-size: 120%;
			color: red;
			}
	</style>
	<head>	<body class='summary'>	<title>AIDMOR Report Summary</title>
	<table  class='summary'><tr style="background-color:#084B8A">
	<td><font   size="4" color="white">AIDMOR Summary Report</font>
	<img src="http://www.airmethods.com/images/default-source/Defenders-Of-Tomorrow/am-logo-defenders-of-tomorrow.png?sfvrsn=6" align="right">
	</td></tr></table>
	<p class="test">THIS AIDMOR WAS CREATED WITHIN THE TESTING PHASE AND IS ONLY A TEST.</p>
	"""

	#summary+="%s</br>" % slurpFieldList( {"AIDMOR":headerInfo})
	summary+="%s</br>" % slurpField( "ETQ$NUMBER",	0)
	time = thisDocument.getFieldText("EVENT_TIME_2_P")
	if time != None and time !="":
		summary+= "<b>%s</b> %s </br>" %( thisDocument.getField("EVENT_TIME_2_P").getPrompt(), time) 
	summary+="%s</br>" % slurpField( "BRIEF_EVENT_DESCRIPTION_P",	0)
	summary+=slurpSubform(dictSubformAttributes["EVENT"])   # instantiated in onOpen 
	summary+= "</br>%s</br>%s" % (slurpField( "LOCATION_TYPE_2_P",1),slurpField( "DESCRIPTION_8_P",0)	)

	summary+="<table   class='summary'>"	
	
	
	if slurpField( "CITY_2_P",0) !="":
		summary+="<tr><td>%s" %  slurpField( "CITY_2_P",0)
		if slurpField( "STATE_3_P",0) !="":
			summary+= ", %s</td>" % slurpField( "STATE_3_P",1)

	if slurpField( "LATTITUDE_P",0) !="":
		summary+="<td> %s / %s </td></tr>" % (slurpField( "LATTITUDE_P",0) , slurpField( "LONGITUDE_P",0))
	else:
		summary+="</tr>"
		
	if False:
		if slurpField( "LOCATION_OWNER_S_NAME_P",0) !="":
			summary+="<tr><td> %s </td><td>%s </td></tr>" % ( slurpField( "LOCATION_OWNER_S_NAME_P",0), slurpField( "LOCATION_OWNER_NUMBER_P",0))

		if slurpField( "HOSPITAL_NAME_2_P",0) !="":
			summary+="<tr><td>%s</td></tr>" % slurpField( "HOSPITAL_NAME_2_P",0)
		if slurpField( "AIRPORT_ID_P",0) !="":
			summary+="<tr><td>%s</td><td>%s</td></tr>" % (slurpField( "AIRPORT_ID_P",0),slurpField("AIRPORT_NAME_P",0))
		if slurpField( "AMC_BASE_1_P",0) !="":
			summary+="<tr><td>%s</td></tr>" % (slurpField( "AMC_BASE_1_P",0))
		if slurpField( "EVENT_LOCATION_5_P",0) !="":
			summary+="<tr><td>%s</td></tr>" % (slurpField( "EVENT_LOCATION_5_P",1))
		if slurpField( "LOCATION_IS_SECURE_1_P",1) !="":
			summary+="<tr><td>%s</td></tr>" % slurpField( "LOCATION_IS_SECURE_1_P",1)
	else:
		summary+="<tr><td>"
		for fieldList in catList:
			summary+= slurpFieldList( fieldList)
		summary+="</td></tr>"
		
	summary+="</table></span>"
	summary+="%s</br>%s" % (slurpField("SUBMITTED_BY_4_P",0),slurpField("ETQ$LOCATIONS",1))
	
	for cat in ("THREAT", "ERROR"):
		summary+=slurpSubform(dictSubformAttributes[cat]	) # instantiated in onOpen 
	str = thisDocument.getFieldValue("EVENT_DESCRIPTION_4_P")
	if len(str)>0:
		summary+="</br><b>Event Description:</b> %s" %  str
	str= thisDocument.getFieldValue("PREVENATIVE_MEASURES_P")
	if len(str)>0:
		summary+="</br></br><b>Prevenative Measure:</b> %s" %  str
	summary+="</body></html>"
	myLog( summary)
	thisDocument.setFieldValue("EVENT_SUMMARY_P", summary) 

	myLog(" buildSummaryToo Finish")
	return	
