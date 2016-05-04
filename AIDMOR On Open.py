## AIDMOR onOpen
UserID = thisDocument.getFieldValue("ETQ$AUTHOR")
UserName = eccProfileManager.getUserProfile(UserID).getDisplayName()
thisDocument.setFieldValue("SUBMITTED_BY_1_P", UserName)

thisDocument.setFieldValue("EMPLOYEE_P", thisUser.getID())
thisDocument.setFieldValue("EMPLOYEE_ID_P", thisUser.getID())

thisDocument.setFieldValue("EMAIL_P",thisUser.getEmail())
#buildSummary()