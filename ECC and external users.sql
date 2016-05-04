-- users and the groups they are in 
select usr.user_name,
GROUP_CONCAT(GRP.user_name SEPARATOR ";")
from engine.user_settings USR
left join engine.group_members membs on (  USR.USER_ID = membs.MEMBER_user_id  )
left join engine.user_settings GRP on ( membs.user_id = GRP.USER_ID)
where USR.is_group = 0
group by usr.user_name
order by usr.user_name
;

select usr.user_name, usr.user_ID
from engine.user_settings USR
;
select user_number, user_id
from external_data.person_data
;

-- the query pulls a list of groups and associated members
select GRP.user_id ID , GRP.user_name DESCRIPTION,  USR.DISPLAY_NAME USR_DISPLAY, usr.USER_NAME USR_NAME, USR.EMAIL USR_RMAIL, USR.USER_ID
from engine.user_settings GRP
left join engine.group_members membs on (  GRP.USER_ID = membs.user_id  )
left join engine.user_settings USR on ( membs.MEMBER_user_id = USR.USER_ID)
where GRP.IS_GROUP = 1 
and usr.user_name='jbean'
order by GRP.user_name
;

select usr.user_name,usr.email
from engine.user_settings USR
where usr.is_disabled =1
;
select USR.USER_ID ETQ_NUMBER, 	USR.user_Name USERID
from engine.user_settings USR
WHERE USR.user_Name like'jbean'
order by USERID
;

SELECT  USERS.USER_ID ID, USERS.DISPLAY_NAME DESCRIPTION
FROM ENGINE.USER_SETTINGS USERS
WHERE USERS.IS_GROUP = 0 
AND USERS.USER_ID > 0 
AND USERS.IS_INACTIVE = 0
;

SELECT
DISTINCT USERS.USER_ID,
(USERS.LAST_NAME || ', ' || USERS.FIRST_NAME || RTRIM(' ' || IFNULL(USERS.MIDDLE_INITIAL, " "))) NAME,
LTRIM(RTRIM('User')) USER_TYPE,
USERS.DISPLAY_NAME DISPLAY_NAME,
PHASE_SETTINGS.DISPLAY_NAME PHASE_SETTINGS_DISPLAY_NAME
FROM ENGINE.USER_SETTINGS USERS
LEFT JOIN ENGINE.PHASE_SETTINGS PHASE_SETTINGS ON (USERS.ETQ$CURRENT_PHASE = PHASE_SETTINGS.PHASE_ID)
LEFT JOIN ENGINE.ETQ$USER_SETTINGS_LOCS ETQ$USER_SETTINGS_LOCS_1 ON (USERS.USER_ID = ETQ$USER_SETTINGS_LOCS_1.USER_ID)
LEFT JOIN DATACENTER.LOCATION_PROFILE LOCATION_PROFILE_1 ON (ETQ$USER_SETTINGS_LOCS_1.ETQ$LOCATIONS_ID = LOCATION_PROFILE_1.LOCATION_PROFILE_ID)
WHERE USERS.IS_GROUP = 0 AND (USERS.USER_ID > 0) AND USERS.IS_INACTIVE = 0 
;
    
SELECT USERS.USER_ID,
USERS.DISPLAY_NAME NAME,
LTRIM(RTRIM('Group')) USER_TYPE,
USERS.DISPLAY_NAME DISPLAY_NAME
FROM ENGINE.USER_SETTINGS USERS
WHERE USERS.IS_GROUP = 1 AND USERS.IS_INACTIVE = 0
and Users.user_id>0

UNION 
SELECT USERS.USER_ID,
(USERS.LAST_NAME || ', ' || USERS.FIRST_NAME || RTRIM(' ' || IFNULL(USERS.MIDDLE_INITIAL, " "))) NAME,
LTRIM(RTRIM('User')) USER_TYPE,
USERS.DISPLAY_NAME DISPLAY_NAME
FROM ENGINE.USER_SETTINGS USERS
WHERE USERS.IS_GROUP = 0
AND (USERS.USER_ID > 0)
AND USERS.IS_INACTIVE = 0
;

SELECT USERS.USER_ID,
(USERS.LAST_NAME || ', ' || USERS.FIRST_NAME || RTRIM(' ' || IFNULL(USERS.MIDDLE_INITIAL, " "))) NAME,
LTRIM(RTRIM('User')) USER_TYPE,
USERS.DISPLAY_NAME DISPLAY_NAME, USERS.LOCALE_ID, USERS.USER_NAME
FROM ENGINE.USER_SETTINGS USERS
WHERE USERS.IS_GROUP = 0
AND (USERS.USER_ID > 0)
AND USERS.IS_INACTIVE = 0
AND USERS.USER_NAME ='jbean'
 
;

-- this select pulls by group name 
select GRP.DISPLAY_NAME DISPLAY_NAME, GRP.USER_ID GROUP_ID, 
group_concat( person.USER_NUMBER  SEPARATOR ';') MEMBERS, 1 IS_GROUP
FROM ENGINE.USER_SETTINGS GRP        
left join external_data.person_data person on (GRP.DISPLAY_NAME = person.department_14 )
WHERE GRP.IS_GROUP = 1 
-- AND GRP.DISPLAY_NAME in ('Safety')
group by GRP.DISPLAY_NAME
;

-- however everyone is differnt in that there is no prede
SET SESSION group_concat_max_len = 1000000;

SELECT 
GRP.DISPLAY_NAME DISPLAY_NAME , GRP.USER_ID GROUP_ID,
-- group_concat( USR.USER_ID SEPARATOR ';') MEMBERS, 1 IS_GROUP 
 USR.USER_ID
from engine.user_settings USR
cross join ENGINE.USER_SETTINGS GRP 
where USR.IS_GROUP = 0
AND USR.IS_INACTIVE = 0
AND (USR.USER_ID > 0)
AND GRP.DISPLAY_NAME in ('Everyone')
-- group by GRP.DISPLAY_NAME
;

SELECT     COUNT(USR.USER_ID) FROM     engine.user_settings USR ;

SELECT USERS.USER_ID ID
FROM ENGINE.USER_SETTINGS USERS
WHERE USERS.IS_GROUP = 0
AND (USERS.USER_ID > 0)
AND USERS.IS_INACTIVE = 0
 ;
 select count( user_id) from engine.user_settings
 ;
 SELECT USERS.USER_ID ID,
USERS.DISPLAY_NAME  DESCRIPTION,
LTRIM(RTRIM('Group')) USER_TYPE,
USERS.DISPLAY_NAME DISPLAY_NAME
FROM ENGINE.USER_SETTINGS USERS
WHERE USERS.IS_GROUP = 1 AND USERS.IS_INACTIVE = 0
and USERS.USER_ID>0

;
select count( is_group) from engine.user_settings where is_group=1;

select count(distinct mem.user_id) from engine.group_members mem
left join engine.user_settings usr on (usr.user_id = mem.user_id)
where usr.is_group=1;