\f C:\#Git\ReadSQL\ex;
\cs test4.dbx;

ALTER TABLE Moje_TEMP RENAME COLUMN id TO VERTRAG;
ALTER TABLE Moje_TEMP RENAME COLUMN id_p TO PARTNER;
ALTER TABLE Moje_TEMP RENAME COLUMN DISTRIBUTOTT TO DISTRIBUTOR;
ALTER TABLE Moje_TEMP ADD COLUMN DIVISION TEXT;

update Moje_TEMP SET DIVISION = '02' WHERE SPOTREBA_MWH_AKTUALNI_PLYN is NOT NULL;
update Moje_TEMP SET DIVISION =  'E2' WHERE SPOTREBA_MWH_AKTUALNI_EE is NOT NULL;