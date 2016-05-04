SELECT
SQ.AUDIT_DOCUMENT_ID AUDIT_DOCUMENT_ID,
RIGHT( 	LOC.HIERARCHICAL_NAME, 	LENGTH( LOC.HIERARCHICAL_NAME) - LOCATE(":", LOC.HIERARCHICAL_NAME) 	)	LOCATIO_PROFIL_HIERARCHICA_NAM,
DATE_FORMAT(SQ.ETQ$CREATED_DATE ,  '%b %d, %Y' ) 		AUDI_DOCUMENT_ETQ$CREATED_DATE,
DATE_FORMAT(SQ.ETQ$COMPLETED_DATE ,  '%b %d, %Y' ) 		AUDI_DOCUMEN_ETQ$COMPLETE_DATE,
LEFT(LOC.HIERARCHICAL_NAME , 	LOCATE(":",  LOC.HIERARCHICAL_NAME)-1)	 REGION,
SQ.DESCRIPTION APPLICAB_AUDI_TYP_1_DESCRIPTIO,
SQ.SECTION_TITLE LOCATION_PROFILE_SECTION_TITLE,
IF (SQ.ETQ$LOCATIONS_ID IS NULL,"Missing", 	IF (SQ.ETQ$COMPLETED_DATE IS NULL,"In Process","Complete" ) 	) WORKING,
USR.DISPLAY_NAME USER_SETTINGS_1_DISPLAY_NAME,
SQ.ETQ$CREATED_DATE LOC_ETQ$CREATED_DATE,
SQ.ETQ$COMPLETED_DATE LOC_ETQ$COMPLETED_DATE

FROM
DATACENTER.LOCATION_PROFILE LOC
LEFT JOIN (
	SELECT AUDTYPE.DESCRIPTION, AUD.ETQ$LOCATIONS_ID, DOC.AUDIT_DOCUMENT_ID, DOC.SECTION_TITLE, DOC.ETQ$CREATED_DATE, DOC.ETQ$COMPLETED_DATE , USR.DISPLAY_NAME   
		from AUDITS.ETQ$AUDIT_DOCUMENT_LOCS AUD      
		INNER JOIN AUDITS.AUDIT_DOCUMENT DOC  ON DOC.AUDIT_DOCUMENT_ID = AUD.AUDIT_DOCUMENT_ID
		INNER JOIN LOOKUPS.APPLICABLE_AUDIT_TYPE AUDTYPE ON DOC.APPLICABLE_ID = AUDTYPE.APPLICABLE_AUDIT_TYPE_ID
		LEFT JOIN ENGINE.USER_SETTINGS USR ON (LOC.ETQ$AUTHOR = USR.USER_ID 
	)

WHERE
DOC.SECTION_TITLE ="2nd Quarter 2015 Base Self Assessment"             )  SQ ON LOC.LOCATION_PROFILE_ID = SQ.ETQ$LOCATIONS_ID 		 
WHERE    LOC.DISABLED  = 0 
AND LOC.HIERARCHICAL_NAME NOT LIKE  "Maintenance 135%" 
AND LOC.HIERARCHICAL_NAME NOT LIKE  "Maintenance 145 Repair Station%" 
AND LOC.HIERARCHICAL_NAME NOT LIKE  "Sundance%" 
AND LOC.HIERARCHICAL_NAME NOT LIKE  "Training Location%" 
AND HIERARCHICAL_NAME NOT LIKE "%Fuel Facility%" 
AND LOC.HIERARCHICAL_NAME NOT LIKE  "Vendor%" 
GROUP BY LOC.LOCATION_PROFILE_ID
**********************

SELECT
SQ.AUDIT_DOCUMENT_ID AUDIT_DOCUMENT_ID,
RIGHT( 	LOC.HIERARCHICAL_NAME, 	LENGTH( LOC.HIERARCHICAL_NAME) - LOCATE(":", LOC.HIERARCHICAL_NAME) 	)	LOCATIO_PROFIL_HIERARCHICA_NAM,
DATE_FORMAT(SQ.ETQ$CREATED_DATE ,  '%b %d, %Y' ) 		AUDI_DOCUMENT_ETQ$CREATED_DATE,
DATE_FORMAT(SQ.ETQ$COMPLETED_DATE ,  '%b %d, %Y' ) 		AUDI_DOCUMEN_ETQ$COMPLETE_DATE,
LEFT(LOC.HIERARCHICAL_NAME , 	LOCATE(":",  LOC.HIERARCHICAL_NAME)-1)	 REGION,
SQ.DESCRIPTION APPLICAB_AUDI_TYP_1_DESCRIPTIO,
SQ.SECTION_TITLE LOCATION_PROFILE_SECTION_TITLE,
IF (SQ.ETQ$LOCATIONS_ID IS NULL,"Missing",
	IF (SQ.ETQ$COMPLETED_DATE IS NULL,"In Process","Complete" ) 	) WORKING
FROM DATACENTER.LOCATION_PROFILE LOC
  LEFT JOIN 
  (SELECT AUDTYPE.DESCRIPTION, AUD.ETQ$LOCATIONS_ID, DOC.AUDIT_DOCUMENT_ID, DOC.SECTION_TITLE, DOC.ETQ$CREATED_DATE, DOC.ETQ$COMPLETED_DATE
   from AUDITS.ETQ$AUDIT_DOCUMENT_LOCS AUD 
    INNER  JOIN AUDITS.AUDIT_DOCUMENT DOC  ON DOC.AUDIT_DOCUMENT_ID = AUD.AUDIT_DOCUMENT_ID
    INNER JOIN LOOKUPS.APPLICABLE_AUDIT_TYPE AUDTYPE ON DOC.APPLICABLE_ID = AUDTYPE.APPLICABLE_AUDIT_TYPE_ID 
   WHERE DOC.SECTION_TITLE ="2nd Quarter 2015 Base Self Assessment"
            )  SQ ON LOC.LOCATION_PROFILE_ID = SQ.ETQ$LOCATIONS_ID
		
WHERE    LOC.DISABLED  = 0
	 AND LOC.HIERARCHICAL_NAME NOT LIKE  "Maintenance 135%"
	 AND LOC.HIERARCHICAL_NAME NOT LIKE  "Maintenance 145 Repair Station%"
	 AND LOC.HIERARCHICAL_NAME NOT LIKE  "Sundance%"
	 AND LOC.HIERARCHICAL_NAME NOT LIKE  "Training Location%"
	 AND HIERARCHICAL_NAME NOT LIKE "%Fuel Facility%"
AND LOC.HIERARCHICAL_NAME NOT LIKE  "Vendor%"
GROUP BY LOC.LOCATION_PROFILE_ID