def getMKL( table, key,cat)
	## sample SQL that is stored in the datasource
	# SELECT TESTMKL.TESTMKL_ID , 
	# SUBSTRING_INDEX( TESTMKL.DESCRIPTION ,'~',-1) DESCRIPTION
	# FROM LOOKUPS.TESTMKL TESTMKL   
	# For example, if the "item" field contains "009378M38293," then:
	# LEFT(`item`, LOCATE("M", `item`)-1) is the same as LEFT(`item`, 6) which returns "009378."
	sql = """
	SELECT ETQ$TABLE_NAME.ETQ$TABLE_KEY  ID, 
	ETQ$TABLE_NAME.DESCRIPTION DESCRIPTION
	FROM LOOKUPS.ETQ$TABLE_NAME TESTMKL
	WHERE ETQ$TABLE_NAME.DESCRIPTION LIKE "ETQ$WHERE_LIKE"  
	"""
	param = {
		"ETQ$TABLE_NAME":table,
		"ETQ$TABLE_KEY": key,
		"ETQ$WHERE_LIKE": cat
	}
	dao = thisApplication.executeQueryFromDatasource("MKL_LOOKUP_P", param)
	dict={}
	while dao.next():		## next will start at the first entry and iterate through
		dict[dao.getValue("ID")] = dao.getValue("DESCRIPTION")
		
	return dict
	
cat = thisDocument.getFieldValue("AAATEXT_P")
org=thisDocument.getDisplayValue("ORG_1_P")	
cat="AMC~%s~EVENT~" %(org)
mklDict = getMKL( "TESTMKL","TESTMKL_ID", cat)

# from the dict build a list of events
# break the string on the tilde
currentKey =""
for key, value in mklDict:
	list = value.split('~')
	newKey= "%s~%s~%s" % (list[0],list[1],list[2])
	if  newKey == currentKey:
		continue
	currentKey = newKey
	
	
