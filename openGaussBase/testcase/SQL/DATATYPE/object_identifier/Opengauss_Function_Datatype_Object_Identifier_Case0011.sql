-- @testpoint:正常建行存表（分区表）及数据插入
drop table if exists object_identifier_011;
CREATE TABLE object_identifier_011(
	c1 OID,
	c2 CID,
	c3 XID,
	c4 TID,
	c5 REGCONFIG,
	c6 REGDICTIONARY,
	c7 REGOPER,
	c8 REGOPERATOR,
	c9 REGPROC,
	c10 REGPROCEDURE,
	c11 REGCLASS,
	c12 REGTYPE
	c13 int
)
WITH (orientation=row, compression=no)
PARTITION BY RANGE (c13)
(
        PARTITION P1 VALUES LESS THAN(5000),
        PARTITION P2 VALUES LESS THAN(10000),
        PARTITION P3 VALUES LESS THAN(15000),
        PARTITION P4 VALUES LESS THAN(20000),
        PARTITION P5 VALUES LESS THAN(25000),
        PARTITION P6 VALUES LESS THAN(30000),
        PARTITION P7 VALUES LESS THAN(40000),
        PARTITION P8 VALUES LESS THAN(MAXVALUE)
)
;
select * from object_identifier_011;
drop table if exists object_identifier_011;