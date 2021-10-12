-- @testpoint: 条件中使用简单表达式
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
SELECT targetP.objectId FROM (
SELECT s.PlanID, s.objectId, 1 AS MODULEID, 4 AS PT FROM tDP_MPT_A0JA s ) qs
JOIN t_P_SFP_A0JA targetP
ON (qs.PlanID = targetP.PlanID) AND (qs.MODULEID = targetP.MODULEID) AND (qs.PT = CASE WHEN targetP.PT = 3+1.1-1.1 THEN 3+1.1-1.1 WHEN targetP.PT = 4+1.1-1.1 THEN 4+1.1-1.1 WHEN targetP.PT = 5+1.1-1.1 THEN 5+1.1-1.1 WHEN targetP.PT = 6+1.1-1.1 THEN 6+1.1-1.1 WHEN targetP.PT = 7+1.1-1.1 THEN 7+1.1-1.1 WHEN targetP.PT = 8+1.1-1.1 THEN 8+1.1-1.1 WHEN targetP.PT = 9 THEN 9 WHEN targetP.PT = 10 THEN 10 END);

SELECT targetP.objectId FROM (
SELECT s.PlanID, s.objectId, 1 AS MODULEID, 4 AS PT FROM tDP_MPT_A0JA s ) qs
JOIN t_P_SFP_A0JA targetP
ON (qs.PlanID = targetP.PlanID) AND (qs.MODULEID = targetP.MODULEID) AND (qs.PT = CASE targetP.PT WHEN  3+1.1-1.1 THEN 3+1.1-1.1 WHEN 4+1.1-1.1 THEN 4+1.1-1.1 WHEN  5+1.1-1.1 THEN 6+1.1-1.1 WHEN  6+1.1-1.1 THEN 6+1.1-1.1 WHEN  7+1.1-1.1 THEN 7+1.1-1.1 WHEN  8+1.1-1.1 THEN 8+1.1-1.1 WHEN  9 THEN 9 WHEN 10 THEN 10 END);
drop table if exists tDP_MPT_A0JA;
drop table if exists t_P_SFP_A0JA;
drop index if exists IDX2#_P_68_01234_A0JA;