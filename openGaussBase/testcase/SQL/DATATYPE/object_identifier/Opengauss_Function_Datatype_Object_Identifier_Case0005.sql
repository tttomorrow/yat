-- @testpoint:插入非法空值,合理报错；
drop table if exists object_identifier_005;
CREATE  TABLE object_identifier_005(
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
);
insert into object_identifier_005 values (' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ');
drop table if exists object_identifier_005;