SELECT
MCS.MCS_ID MCS_ID,
MCS.AIRCRAFT_ID_3 MCS_AIRCRAFT_ID_3,
IFNULL(OPEN_1.DESCRIPTION,'[ NOT SET ]') OPEN_1_DESCRIPTION,
MCS.MX_RELEASE MCS_MX_RELEASE,
TIER_STATUS.DESCRIPTION TIER_STATUS_DESCRIPTION,
MCS.REVISED_RTS MCS_REVISED_RTS,
USER_SETTINGS.DISPLAY_NAME USER_SETTINGS_DISPLAY_NAME,
MCS.CONTACT MCS_CONTACT,
MCS.BASE_LOCATION MCS_BASE_LOCATION,
MCS.OPEN_CLOSED_NOTES MCS_OPEN_CLOSED_NOTES,
MCS.ETQ$CREATED_DATE MCS_ETQ$CREATED_DATE,
CASE BOOLEAN_VALUES_1.DESCRIPTION  	when 'Yes' then 'common/images/flag.png' 	else 'common/images/blank.png' 	end BOOLEAN_VALUES_1_DESCRIPTION,
MCS.PRIMARY_MX_2 MCS_PRIMARY_MX_2,
MCS.OOS_REASON MCS_OOS_REASON,
BOOLEAN_VALUES_2.DESCRIPTION BOOLEAN_VALUES_2_DESCRIPTION,
MCS.OTHER_DISCRPANCY MCS_OTHER_DISCRPANCY,
CAUGHT_DISCREPANCY_2.DESCRIPTION CAUGH_DISCREPANC_2_DESCRIPTION

FROM	AMC_OCC.MCS MCS
LEFT JOIN
LOOKUPS.OPEN OPEN_1 ON (MCS.OPEN_ID = OPEN_1.OPEN_ID )

LEFT JOIN
LOOKUPS.TIER_STATUS TIER_STATUS ON (MCS.TIER_2_STATUS_ID = TIER_STATUS.TIER_STATUS_ID )

LEFT JOIN
ENGINE.USER_SETTINGS USER_SETTINGS ON (MCS.ETQ$AUTHOR = USER_SETTINGS.USER_ID )

LEFT JOIN
ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES_1 ON (MCS.FLAG_REPORT_ID = BOOLEAN_VALUES_1.VALUE )

LEFT JOIN
ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES_2 ON (MCS.CAUGHT_DISCREPANCY_1_ID = BOOLEAN_VALUES_2.VALUE )

LEFT JOIN
AMC_OCC.CAUGHT_DISCREPANCY CAUGHT_DISCREPANCY_3 ON (MCS.MCS_ID = CAUGHT_DISCREPANCY_3.MCS_ID )

LEFT JOIN
LOOKUPS.CAUGHT_DISCREPANCY CAUGHT_DISCREPANCY_2 ON (CAUGHT_DISCREPANCY_3.CAUGHT_DISCREPANCY_ID = CAUGHT_DISCREPANCY_2.CAUGHT_DISCREPANCY_ID )

WHERE 
	BOOLEAN_VALUES_2.DESCRIPTION = 'Yes'
	AND 	MCS.ETQ$CREATED_DATE 	
	
	between    MAKEDATE(YEAR(CURDATE() ), 1) + INTERVAL QUARTER(CURDATE() ) QUARTER  - INTERVAL  2 QUARTER   
		AND 	MAKEDATE(YEAR(CURDATE() ), 1) + INTERVAL QUARTER(CURDATE() ) QUARTER  - INTERVAL  1 QUARTER 		

		BETWEEN "2015-04-01" AND "2015-07-01"





MCS.ETQ$CREATED_DATE  BETWEEN (CURDATE() - INTERVAL 90 DAY) AND CURDATE()
SELECT  between ( MAKEDATE(YEAR(CURDATE()), 1) + INTERVAL QUARTER(CURDATE()) QUARTER  - INTERVAL    1 QUARTER , MAKEDATE(YEAR(CURDATE()), 1) + INTERVAL QUARTER(CURDATE()) QUARTER  - INTERVAL    2 QUARTER 


////