\f test;
\s test.dbx;

drop table if exists test4;

create table test4 (GENDER_TXT text, TITLE_ACA1T text, VEK int, ZZDEATHDT datetime, BPCONTFCT_ORG text, LEGAL_ENTYT text, ZAMESTNANEC text, DLUZNIK text, BONITA_OP_Sum int, POCET_SMLUV_PLYN int, POCET_SMLUV_PLYN_AKTIVNI int, POCET_SMLUV_PLYN_VAKTIVACI int, POCET_SMLUV_EE int, POCET_SMLUV_EE_AKTIVNI int, POCET_SMLUV_EE_VAKTIVACI int, EINZDAT datetime, AUSZDAT datetime, DIVISIONT text, C_ABSZYKT text, UCACTDETIDT text, UCCON_CLAST text, DISTRIBUTOTT text, SPOTREBA_MWH_AKTUALNI_PLYN real, SPOTREBA_MWH_AKTUALNI_EE real, ZZEDIRATE text, ZZVBSARTT text, MS_REGIONT text, MS_COMMU_CODE text, MS_krajn text, MS_okresn text, MS_POCET_OBYVATEL int, OP_REGIONT text, OP_COMMU_CODE int, KA_REGIONT text, KA_COMMU_CODE int, WU_branch text, WU_distance real, WU_duration int, id_p int, id int);

\r test4.csvx, "	";
\i test4;
