\cms GDPR;

DECLARE @query       AS NVARCHAR(MAX),
	@query2       AS NVARCHAR(MAX),
        @OPTOUTS_DATA  NVARCHAR(MAX),
        @OPTINS_DATA  NVARCHAR(MAX),
	@GDPRRES_DATA NVARCHAR(MAX),
        @PIVOT  NVARCHAR(MAX),
	@RSN_COLS NVARCHAR(MAX),
	@COLS NVARCHAR(MAX),
	@FIN NVARCHAR(MAX)

SET @OPTOUTS_DATA = Stuff((SELECT DISTINCT ',SUM(case when C_GDPR_PU='''+d.C_GDPR_PU+ ''' THEN 1 ELSE NULL END) AS [OPTOUT_'+ d.C_GDPR_PU + ']'
                          FROM  (select distinct C_GDPR_PU from "GDPR_PUCH" where CONVERT(INT,CASE WHEN IsNumeric(CONVERT(VARCHAR(12), RIGHT(C_GDPR_PU,2))) = 1 THEN CONVERT(VARCHAR(12),RIGHT(C_GDPR_PU,2)) ELSE 0 END)  < 22) d
                          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')

SET @OPTINS_DATA = Stuff((SELECT DISTINCT ','+d.C_GDPR_PU+' as OPTIN_'+d.C_GDPR_PU
                          FROM (select distinct C_GDPR_PU from "GDPR_PUCH" where CONVERT(INT,CASE WHEN IsNumeric(CONVERT(VARCHAR(12), RIGHT(C_GDPR_PU,2))) = 1 THEN CONVERT(VARCHAR(12),RIGHT(C_GDPR_PU,2)) ELSE 0 END)  < 22) d
                          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')

SET @GDPRRES_DATA = Stuff((SELECT DISTINCT ','+d.C_GDPR_PU+' as GDPR_'+d.C_GDPR_PU
                          FROM (select distinct C_GDPR_PU from "GDPR_PUCH" where CONVERT(INT,CASE WHEN IsNumeric(CONVERT(VARCHAR(12), RIGHT(C_GDPR_PU,2))) = 1 THEN CONVERT(VARCHAR(12),RIGHT(C_GDPR_PU,2)) ELSE 0 END) < 22) d
                          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')

SET @COLS = STUFF((SELECT ',[' + d.C_GDPR_PU +']'
                      FROM (select distinct C_GDPR_PU from "GDPR_PUCH" where CONVERT(INT,CASE WHEN IsNumeric(CONVERT(VARCHAR(12), RIGHT(C_GDPR_PU,2))) = 1 THEN CONVERT(VARCHAR(12),RIGHT(C_GDPR_PU,2)) ELSE 0 END) < 22) d
                          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')

SET @RSN_COLS = STUFF((SELECT ',[RSN_' + d.C_GDPR_PU +']'
                      FROM (select distinct C_GDPR_PU from "GDPR_PUCH" where CONVERT(INT,CASE WHEN IsNumeric(CONVERT(VARCHAR(12), RIGHT(C_GDPR_PU,2))) = 1 THEN CONVERT(VARCHAR(12),RIGHT(C_GDPR_PU,2)) ELSE 0 END) < 22) d
                          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')


SET @FIN = Stuff((SELECT DISTINCT  ',case when OPTIN_'+d.C_GDPR_PU+ ' is not null and OPTOUT_'+d.C_GDPR_PU+ ' is null and GDPR_'+d.C_GDPR_PU+' is not null then GDPR_'+d.C_GDPR_PU+' else 0 end as '+d.C_GDPR_PU+
			  ',case when OPTOUT_'+d.C_GDPR_PU+ ' is not null then 98 when (GDPR_ZPU07>0 and GDPR_ZPU08>0 and GDPR_ZPU09>0 and GDPR_ZPU10>0 and GDPR_ZPU11>0 and GDPR_ZPU13>0 and coalesce(GDPR_ZPU01,GDPR_ZPU02,GDPR_ZPU03,GDPR_ZPU04,GDPR_ZPU05,GDPR_ZPU06,GDPR_ZPU15,GDPR_ZPU16,GDPR_ZPU17,GDPR_ZPU18,GDPR_ZPU19,GDPR_ZPU20,GDPR_ZPU21) is null) then 2 when GDPR_'+d.C_GDPR_PU+'>0 then 3 else 99  end as RSN_' + d.C_GDPR_PU
                          FROM (select distinct C_GDPR_PU from "GDPR_PUCH" where CONVERT(INT,CASE WHEN IsNumeric(CONVERT(VARCHAR(12), RIGHT(C_GDPR_PU,2))) = 1 THEN CONVERT(VARCHAR(12),RIGHT(C_GDPR_PU,2)) ELSE 0 END)  <22) d
                          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')

set @query2='
select a.* into dbo.GDPR from
(select GDPR_ID, CHANNEL, CHANNEL_CRM, PU, RSN, DATE, TXTMD  from (select GDPR_ID, CHANNEL, CHANNEL_CRM, PU, RSN, DATEADD(day, date, 0) as DATE  from ( select *  from (select GDPR_ID, CHANNEL, CHANNEL_CRM,
case when substring(indicatorname,1,3)=''RSN'' then concat(''ZPU'',substring(indicatorname,8,2)) else concat(''ZPU'',substring(indicatorname,4,2)) end as PU,
case when substring(indicatorname,1,3)=''RSN'' then ''RSN'' else ''DATE'' end as TYPE,
indicatorvalue
from (select T1.C_GDPR_DS as GDPR_ID, T1.C_GDPRCHN as CHANNEL, T1.C_GDPRCHN_CRM as CHANNEL_CRM, '+@FIN+' from (select C_GDPRCHN, '+@OPTINS_DATA+'  from (select C_GDPR_PU, C_GDPRCHN, brm=1 from "GDPR_PUCH") a pivot (max(brm) for [C_GDPR_PU] in ('+@COLS+')) piv ) T0
LEFT JOIN (
SELECT *
		 FROM (select b.C_GDPRCHN, b.C_GDPRCHN_CRM, join1.* from
(select C_GDPR_DS, '+ @GDPRRES_DATA+'  from (select C_GDPR_DS, C_GDPR_PU, brm=1, datediff(day,''1900-1-1'',C_PLAT_DO) as C_PLAT_DO from "GDPR_RES" where C_PLAT_DO>GETDATE() and C_PLAT_OD<GETDATE()  ) a pivot (max(C_PLAT_DO) for [C_GDPR_PU] in  ('+@COLS+')) piv ) join1
inner join (
select C_GDPR_DS, C_GDPRCHN=''CHT'', C_GDPRCHN_CRM=''C'' from "GDPR_RES" where C_GDPR_PU!=''ZDEF''
union
select C_GDPR_DS, C_GDPRCHN=''I24'', C_GDPRCHN_CRM=''I'' from "GDPR_RES" where C_GDPR_PU!=''ZDEF''
union
select C_GDPR_DS, C_GDPRCHN=''INT'', C_GDPRCHN_CRM=''E'' from "GDPR_RES" where C_GDPR_PU!=''ZDEF''
union
select C_GDPR_DS, C_GDPRCHN=''LET'', C_GDPRCHN_CRM=''P'' from "GDPR_RES" where C_GDPR_PU!=''ZDEF''
union
select C_GDPR_DS, C_GDPRCHN=''PAG'', C_GDPRCHN_CRM=''S'' from "GDPR_RES" where C_GDPR_PU!=''ZDEF''
union
select C_GDPR_DS, C_GDPRCHN=''PERSONAL'', C_GDPRCHN_CRM=''O'' from "GDPR_RES" where C_GDPR_PU!=''ZDEF''
union
select C_GDPR_DS, C_GDPRCHN=''TEL'', C_GDPRCHN_CRM=''T'' from "GDPR_RES" where C_GDPR_PU!=''ZDEF''
) b
on join1.C_GDPR_DS=b.C_GDPR_DS
left join
(select C_GDPRCHN, '+@OPTINS_DATA+'   from (select C_GDPR_PU, C_GDPRCHN, brm=1 from "GDPR_PUCH") a pivot (max(brm) for [C_GDPR_PU] in ('+@COLS+')) piv ) d
on b.C_GDPRCHN=d.C_GDPRCHN) T0) T1
ON (T0."C_GDPRCHN" = T1."C_GDPRCHN")
left join
(SELECT
C_GDPR_DS, C_GDPRCHN, '+@OPTOUTS_DATA+' FROM
"GDPR_OPTIO" T2_BP
left join
(select distinct C_GDPR_DS, C_GDPR_BP from "GDPR_RES" where C_GDPR_PU!=''ZDEF'') T2_DS
on T2_BP.C_GDPR_BP=T2_DS.C_GDPR_BP
group by C_GDPRCHN, C_GDPR_DS) T2
on T1.C_GDPRCHN=T2.C_GDPRCHN and T1.C_GDPR_DS=T2.C_GDPR_DS) a
unpivot
(
  indicatorvalue
  for indicatorname in ('+@COLS+','+@RSN_COLS+')
) unpiv ) a
PIVOT
(min(indicatorvalue)
for TYPE in ([RSN],[DATE])) piv ) def
) a
left join
(select a.TXTMD,b.C_GDPR_PU from (select distinct TXTMD from "TX39") a
left join
"TX39" b
on b.TXTMD=a.TXTMD
where a.TXTMD<>'''' and b.C_GDPRSEG=''B2C'') b
on a.PU=b.C_GDPR_PU) a
'

IF OBJECT_ID('dbo.GDPR', 'U') IS NOT NULL
  DROP TABLE dbo.GDPR

SET ANSI_WARNINGS OFF

execute (@query2)
