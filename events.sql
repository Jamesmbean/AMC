select ETE.CATEGORY_6 DESCRIPTION, ETE.POSITION POS
from  ETQ$APPLICATION.event_thereat_error ETE
left join LOOKUPS.COMPANY_1 comp on ( ETE.COMPANY_3_ID = comp.COMPANY_1_ID)
left join LOOKUPS.ORG ORG on ( ETE.DIVISION_ID = ORG.ORG_ID)
left join LOOKUPS.EVENT_THREAT_ERROR evther on ( ETE.EVENT_THREAT_ERROR_ID = evther.EVENT_THREAT_ERROR_ID)
where disabled_id = 0
AND comp.description = 'AMC'
AND ORG.description = 'OPS'
AND  evther.description = 'EVENT'
order by ETE.position, ETE.CATEGORY_6
group by ETE.CATEGORY_6 DESCRIPTION