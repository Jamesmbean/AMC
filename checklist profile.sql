SELECT
-- cpname.description descr,
CP.CHECKLIST_PROFILE_ID   CPID,
APPLICABLE_AUDIT_TYPE_1.DESCRIPTION APPLICAB_AUDI_TYP_1_DESCRIPTIO ATDESCR,
QPI.APPLICABLE_AREAS_3 appl_area,
QPI.applicable_system_elements appl_syselem,
QPI.QUESTION_1 q1, 

-- CP.ETQ$NUMBER CHECKLIST_PROFILE_ETQ$NUMBER, 
-- CP.ETQ$CREATED_DATE CHECKLIS_PROFIL_ETQ$CREATE_DAT,
-- USER_SETTINGS_1.DISPLAY_NAME USER_SETTINGS_1_DISPLAY_NAME,
CP.CHECKLIST_PROFILE_NAME CPNAME,

-- USER_SETTINGS_2.DISPLAY_NAME USER_SETTINGS_2_DISPLAY_NAME,
CP.ETQ$MODIFIED_DATE CPMODDATE

FROM AUDITS.CHECKLIST_PROFILE CP
LEFT JOIN ENGINE.USER_SETTINGS USER_SETTINGS_1 ON (CP.ETQ$AUTHOR = USER_SETTINGS_1.USER_ID )
LEFT JOIN LOOKUPS.APPLICABLE_AUDIT_TYPE APPLICABLE_AUDIT_TYPE_1 ON (CP.TYPE_ID = APPLICABLE_AUDIT_TYPE_1.APPLICABLE_AUDIT_TYPE_ID )
LEFT JOIN ENGINE.USER_SETTINGS USER_SETTINGS_2 ON (CP.ETQ$LAST_EDITOR = USER_SETTINGS_2.USER_ID )
LEFT JOIN AUDITS.QUESTION_PROFILE   Qs on (	CP.CHECKLIST_PROFILE_ID	= Qs.QUESTION_PROFILE_ID)
left join lookups.checklist_profile cpname on (CP.CHECKLIST_PROFILE_ID = cpname.CHECKLIST_PROFILE_ID)
left join AUDITS.question_profilesinfo QPI on (CP.CHECKLIST_PROFILE_ID = QPI.CHECKLIST_PROFILE_ID)

where APPLICABLE_AUDIT_TYPE_1.DESCRIPTION <>'' ;