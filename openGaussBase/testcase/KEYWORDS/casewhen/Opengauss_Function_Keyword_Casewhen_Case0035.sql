-- @testpoint: 建表
drop table if exists tDP_MPT_A0JA;
drop table if exists t_P_SFP_A0JA;
drop index if exists IDX2#_P_68_01234_A0JA;

create table tDP_MPT_A0JA
  (PlanID  INTEGER  NOT NULL,
   PHYID   INTEGER  NOT NULL,
   CMENEID INTEGER  NOT NULL,
   entityMoOpId INTEGER  NOT NULL,
   objectId INTEGER  NOT NULL,
   opType CHAR,
   dataArea CHAR  NOT NULL,
   savePointID INTEGER  NOT NULL,
   bufferID INTEGER,
   reservedInt INTEGER,
   reservedInt2 INTEGER,
   reservedString VARCHAR(255),
   BRDSPEC VARCHAR(256),
   CN INTEGER,
   MPTWORKMODE INTEGER,
   OVERLOADALMCLRTHLD INTEGER,
   OVERLOADALMRPTTHLD INTEGER,
   SN INTEGER,
   SRN INTEGER,
   TYPE INTEGER);
insert into tDP_MPT_A0JA
(PlanID, PHYID, CMENEID, entityMoOpId,objectId,opType,dataArea,savePointID,bufferID,reservedInt,BRDSPEC,CN,MPTWORKMODE,OVERLOADALMCLRTHLD,OVERLOADALMRPTTHLD,SN,SRN,TYPE)
values(2,1,1,0,42,'M','I',-1,10,0,'UMPTa/b',0,0,85,90,7,0,1);

create table t_P_SFP_A0JA
  (PlanID  INTEGER  NOT NULL,
   PHYID   INTEGER  NOT NULL,
   CMENEID INTEGER  NOT NULL,
   entityMoOpId INTEGER,
   objectId INTEGER  NOT NULL,
   CN INTEGER  NOT NULL,
   MODULEID INTEGER,
   PT INTEGER  NOT NULL,
   SN INTEGER,
   SRN INTEGER);
insert into t_P_SFP_A0JA(PlanID, PHYID, CMENEID, entityMoOpId,objectId,CN,MODULEID,PT,SN,SRN) values(2,1,1,0,162,0,1,4,7,0 );

CREATE INDEX IDX2#_P_68_01234_A0JA ON T_P_SFP_A0JA(PLANID, PHYID, CN, SRN, SN, MODULEID, PT);
drop table if exists tDP_MPT_A0JA;
drop table if exists t_P_SFP_A0JA;
drop index if exists IDX2#_P_68_01234_A0JA;