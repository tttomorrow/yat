-- @testpoint:正常临时表（行存表）及数据插入；
drop table if exists object_identifier_012;
CREATE TEMPORARY TABLE object_identifier_012(
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
)
WITH (orientation=row, compression=no);
select * from object_identifier_012;
drop table if exists object_identifier_012;