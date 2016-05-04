SELECT
AVT.AVT_ID AVT_ID,
AVT.AIRCRAFT_4 AVT_AIRCRAFT_4,
AVT.INITIAL_DESCRIPTION AVT_INITIAL_DESCRIPTION,
CLASSIFICATION.DESCRIPTION CLASSIFICATION_DESCRIPTION,
AVT.ETQ$CREATED_DATE AVT_ETQ$CREATED_DATE,
AVT.CONTACT_MECHANIC AVT_CONTACT_MECHANIC,
AVT.BASE_1 AVT_BASE_1,
AVT.REGION AVT_REGION,
AVT.PROGRAM AVT_PROGRAM,
BOOLEAN_VALUES.DESCRIPTION BOOLEAN_VALUES_DESCRIPTION,
AVT.ETQ$NUMBER_ONLY AVT_ETQ$NUMBER_ONLY

FROM AMC_OCC.AVT AVT
LEFT JOIN LOOKUPS.CLASSIFICATION CLASSIFICATION ON (AVT.CLASSIFICATION_ID = CLASSIFICATION.CLASSIFICATION_ID )
LEFT JOIN AMC_OCC.ACTIVITY ACTIVITY ON (AVT.AVT_ID = ACTIVITY.AVT_ID )
LEFT JOIN ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES ON (ACTIVITY.FINAL_ID = BOOLEAN_VALUES.VALUE )
LEFT JOIN
LOOKUPS.AVT_TIER AVT_TIER ON (AVT.AVT_TIER_ID = AVT_TIER.AVT_TIER_ID )

WHERE   NOT EXISTS (
	SELECT		1
	FROM AMC_OCC.AVT AVT2
	LEFT JOIN LOOKUPS.CLASSIFICATION CLASSIFICATION ON (AVT2.CLASSIFICATION_ID = CLASSIFICATION.CLASSIFICATION_ID )
	LEFT JOIN AMC_OCC.ACTIVITY ACTIVITY ON (AVT2.AVT_ID = ACTIVITY.AVT_ID )
	LEFT JOIN ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES ON (ACTIVITY.FINAL_ID = BOOLEAN_VALUES.VALUE )
 	WHERE AVT.ETQ$NUMBER = AVT2.ETQ$NUMBER
    AND BOOLEAN_VALUES.DESCRIPTION ='Yes'
)
and AVT_TIER.DESCRIPTION = 'A2'
group by AVT.ETQ$NUMBER_ONLY

;

	SELECT	
    AVT.AVT_ID AVT_ID,
	AVT.AIRCRAFT_4 AVT_AIRCRAFT_4,
	AVT.INITIAL_DESCRIPTION AVT_INITIAL_DESCRIPTION,
	CLASSIFICATION.DESCRIPTION CLASSIFICATION_DESCRIPTION,
	AVT.ETQ$CREATED_DATE AVT_ETQ$CREATED_DATE,
	AVT.CONTACT_MECHANIC AVT_CONTACT_MECHANIC,
	AVT.BASE_1 AVT_BASE_1,
	AVT.REGION AVT_REGION,
	AVT.PROGRAM AVT_PROGRAM,
	BOOLEAN_VALUES.DESCRIPTION BOOLEAN_VALUES_DESCRIPTION,
	AVT.ETQ$NUMBER_ONLY AVT_ETQ$NUMBER_ONLY
	FROM AMC_OCC.AVT AVT
	LEFT JOIN LOOKUPS.CLASSIFICATION CLASSIFICATION ON (AVT.CLASSIFICATION_ID = CLASSIFICATION.CLASSIFICATION_ID )
	LEFT JOIN AMC_OCC.ACTIVITY ACTIVITY ON (AVT.AVT_ID = ACTIVITY.AVT_ID )
	LEFT JOIN ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES ON (ACTIVITY.FINAL_ID = BOOLEAN_VALUES.VALUE )
 	WHERE BOOLEAN_VALUES.DESCRIPTION ='Yes'
;
	SELECT	
	BOOLEAN_VALUES.DESCRIPTION BOOLEAN_VALUES_DESCRIPTION,
	AVT.ETQ$NUMBER_ONLY AVT_ETQ$NUMBER_ONLY
    
	FROM AMC_OCC.AVT AVT
	LEFT JOIN LOOKUPS.CLASSIFICATION CLASSIFICATION ON (AVT.CLASSIFICATION_ID = CLASSIFICATION.CLASSIFICATION_ID )
	LEFT JOIN AMC_OCC.ACTIVITY ACTIVITY ON (AVT.AVT_ID = ACTIVITY.AVT_ID )
	LEFT JOIN ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES ON (ACTIVITY.FINAL_ID = BOOLEAN_VALUES.VALUE )
 	WHERE BOOLEAN_VALUES.DESCRIPTION ='Yes'

