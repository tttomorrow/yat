-- @testpoint:数据插入；
drop table if exists object_identifier_002;
CREATE  TABLE object_identifier_002(
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
insert into object_identifier_002 values (564182,null,null,null,'english','simple',null,'*(integer,integer)',null,'sum(int4)','pg_type','integer');
select * from object_identifier_002;
drop table if exists object_identifier_002;