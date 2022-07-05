\cms GDPR;

\# "SELECT T0."GDPR_ID" AS "C_GDPR_DS",T0.CHANNEL AS CHANNEL,T0."CHANNEL_CRM" AS "CHANNEL_CRM",
T0.PU AS PU,T0.RSN AS RSN,T0."DATE" AS "DATE",T0.TXTMD AS TXTMD,
ROW_NUMBER() OVER ( PARTITION BY T0."GDPR_ID" ORDER BY T0."DATE" DESC) AS "ROW_NUMBER"
FROM "dbo".GDPR T0 WHERE
(((T0.PU = N'ZPU20') AND (T0."CHANNEL_CRM" = N'T')) AND
(T0."DATE" >= CONVERT(DATETIME, CAST(GETDATE() AS DATE), 120)))";

SELECT T0."GDPR_ID" AS "C_GDPR_DS",T0.CHANNEL AS CHANNEL,T0."CHANNEL_CRM" AS "CHANNEL_CRM",
T0.PU AS PU,T0.RSN AS RSN,T0."DATE" AS "DATE",T0.TXTMD AS TXTMD,
ROW_NUMBER() OVER ( PARTITION BY T0."GDPR_ID" ORDER BY T0."DATE" DESC, T0."CHANNEL_CRM") AS "ROW_NUMBER"
FROM "dbo".GDPR T0 WHERE
(((T0.PU = N'ZPU20')) AND
(T0."DATE" >= CONVERT(DATETIME, CAST(GETDATE() AS DATE), 120)));