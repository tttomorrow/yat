-- @testpoint:正常临时表（列存表）及数据插入；
drop table if exists object_identifier_013;
CREATE TEMPORARY TABLE object_identifier_013(
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
WITH (orientation=COLUMN, compression=no);
select * from object_identifier_013;
drop table if exists object_identifier_013;