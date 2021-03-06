SELECT
BOOLEAN_VALUES_1.DESCRIPTION BOOLEAN_VALUES_1_DESCRIPTION,		
group_concat(LOCATION_PROFILE_1.HIERARCHICAL_NAME separator '\n\n') as LOCATI_PROFI_1_HIERARCHICA_NAM,		
IEP_CAPA.CAPA_ISSUER IEP_CAPA_CAPA_ISSUER,		
IEP_CAPA.DATE IEP_CAPA_DATE,		
IEP_CAPA.DESCRIPTION_OF_PROBLEM IE_CAPA_DESCRIPTION_OF_PROBLEM,		
IEP_CAPA.DUE_DATE_1 IEP_CAPA_DUE_DATE_1,		
IEP_CAPA.ETQ$CREATED_DATE IEP_CAPA_ETQ$CREATED_DATE,		
IEP_CAPA.ETQ$NUMBER IEP_CAPA_ETQ$NUMBER,		
IEP_CAPA.IEP_CAPA_ID IEP_CAPA_ID,		
IEP_CAPA.IMPACT_COPY IEP_CAPA_IMPACT_COPY,		
IEP_CAPA.INITIAL_COLOR 		IEP_CAPA_INITIAL_COLOR,
IEP_CAPA.INITIAL_RAC_COLOR IEP_CAPA_INITIAL_RAC_COLOR,		
IEP_CAPA.INITIAL_RESPONSE_DATE IEP_CAPA_INITIAL_RESPONSE_DATE,		
IEP_CAPA.RESIDUAL_COLOR IEP_CAPA_RESIDUAL_COLOR,		
IEP_CAPA.RISK_ITEM_COPY IEP_CAPA_RISK_ITEM_COPY,		
IEP_CAPA.SUBJECT_1 IEP_CAPA_SUBJECT_1,		
if (DATEDIFF(IEP_CAPA.INITIAL_RESPONSE_DATE,  IEP_CAPA.DUE_DATE_1  ) >0, DATEDIFF(IEP_CAPA.INITIAL_RESPONSE_DATE,IEP_CAPA.DUE_DATE_1),"") as DATE_DIFF,		

if( IEP_CAPA.INITIAL_RESPONSE_DATE is NULL ,	
	if( DATEDIFF(IEP_CAPA.DUE_DATE_1, CURDATE() ) <=5 AND DATEDIFF(IEP_CAPA.DUE_DATE_1,CURDATE())  >=0
		,'common/images/yellow-neutral.png',	if( DATEDIFF(IEP_CAPA.DUE_DATE_1, CURDATE()  )<0 , 'common/images/red-sad.png', 'common/images/blank.png' )  		), 
	if(DATEDIFF( IEP_CAPA.INITIAL_RESPONSE_DATE, 	IEP_CAPA.DUE_DATE_1 )>0 , 'common/images/red-sad.png', 'common/images/blank.png')
) as CAPA_LATE,

INITIAL_RAC_1.DESCRIPTION INITIAL_RAC_1_DESCRIPTION,		
INITIAL_RAC_2.DESCRIPTION INITIAL_RAC_2_DESCRIPTION,		
PHASE_SETTINGS.DISPLAY_NAME PHASE_SETTINGS_DISPLAY_NAME,		
RISK_MGMT_EVALUATION_1.DESCRIPTION RIS_MGM_EVALUATIO_1_DESCRIPTIO,	
SOURCE_1.DESCRIPTION SOURCE_1_DESCRIPTION, 
SUBJECT_MATTER_1.DESCRIPTION SUBJECT_MATTER_1_DESCRIPTION,		
USER_SETTINGS_1.DISPLAY_NAME USER_SETTINGS_1_DISPLAY_NAME		

FROM
CORRACT.IEP_CAPA IEP_CAPA
LEFT JOIN
ENGINE.PHASE_SETTINGS PHASE_SETTINGS ON (IEP_CAPA.ETQ$CURRENT_PHASE = PHASE_SETTINGS.PHASE_ID )

LEFT JOIN
CORRACT.ETQ$IEP_CAPA_ASN ETQ$IEP_CAPA_ASN_1 ON (IEP_CAPA.IEP_CAPA_ID = ETQ$IEP_CAPA_ASN_1.IEP_CAPA_ID )

LEFT JOIN
ENGINE.USER_SETTINGS USER_SETTINGS_1 ON (ETQ$IEP_CAPA_ASN_1.ETQ$ASSIGNED = USER_SETTINGS_1.USER_ID )

LEFT JOIN
LOOKUPS.SOURCE SOURCE_1 ON (IEP_CAPA.SOURCE_ID = SOURCE_1.SOURCE_ID ) 

LEFT JOIN
LOOKUPS.INITIAL_RAC INITIAL_RAC_1 ON (IEP_CAPA.INITIAL_RAC_ID = INITIAL_RAC_1.INITIAL_RAC_ID )

LEFT JOIN
CORRACT.ETQ$IEP_CAPA_LOCS ETQ$IEP_CAPA_LOCS_1 ON (IEP_CAPA.IEP_CAPA_ID = ETQ$IEP_CAPA_LOCS_1.IEP_CAPA_ID )

LEFT JOIN
DATACENTER.LOCATION_PROFILE LOCATION_PROFILE_1 ON (ETQ$IEP_CAPA_LOCS_1.ETQ$LOCATIONS_ID = LOCATION_PROFILE_1.LOCATION_PROFILE_ID )

LEFT JOIN
LOOKUPS.SUBJECT_MATTER SUBJECT_MATTER_1 ON (IEP_CAPA.SUBJECT_MATTER_ID = SUBJECT_MATTER_1.SUBJECT_MATTER_ID )

LEFT JOIN
LOOKUPS.RISK_MGMT_EVALUATION RISK_MGMT_EVALUATION_1 ON (IEP_CAPA.RISK_MGMT_EVALUATION_ID = RISK_MGMT_EVALUATION_1.RISK_MGMT_EVALUATION_ID )

LEFT JOIN
ENGINE.BOOLEAN_VALUES BOOLEAN_VALUES_1 ON (IEP_CAPA.IEC_FACILITATED_ID = BOOLEAN_VALUES_1.VALUE )

LEFT JOIN
LOOKUPS.INITIAL_RAC INITIAL_RAC_2 ON (IEP_CAPA.RESIDUAL_RAC_ID = INITIAL_RAC_2.INITIAL_RAC_ID )

WHERE
PHASE_SETTINGS.PHASE_TYPE NOT IN (3) 

GROUP BY IEP_CAPA.IEP_CAPA_ID

