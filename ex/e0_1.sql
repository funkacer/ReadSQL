\f C:\#Git\ReadSQL\ex;
\cms Test;

EXEC sp_RENAME 'Moje_TEMP.id', 'VERTRAG', 'COLUMN';
EXEC sp_RENAME 'Moje_TEMP.id_p', 'PARTNER', 'COLUMN';
EXEC sp_RENAME 'Moje_TEMP.DISTRIBUTOTT', 'DISTRIBUTOR', 'COLUMN';
ALTER TABLE Moje_TEMP ADD DIVISION nvarchar(max);

update Moje_TEMP SET DIVISION = '02' WHERE SPOTREBA_MWH_AKTUALNI_PLYN is NOT NULL;
update Moje_TEMP SET DIVISION = 'E2' WHERE SPOTREBA_MWH_AKTUALNI_EE is NOT NULL;
