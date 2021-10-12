-- @testpoint:数据类型转换至TINYINT\date,合理报错；
drop table if exists object_identifier_004;
CREATE  TABLE object_identifier_004(
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
insert into object_identifier_004 values (564182,null,null,null,'english','simple',null,'*(integer,integer)',null,'sum(int4)','pg_type','integer');
alter table object_identifier_004 alter column c1 TYPE TINYINT;
alter table object_identifier_004 alter column c2 TYPE TINYINT;
alter table object_identifier_004 alter column c3 TYPE TINYINT;
alter table object_identifier_004 alter column c4 TYPE TINYINT;
alter table object_identifier_004 alter column c5 TYPE TINYINT;
alter table object_identifier_004 alter column c6 TYPE TINYINT;
alter table object_identifier_004 alter column c7 TYPE TINYINT;
alter table object_identifier_004 alter column c8 TYPE TINYINT;
alter table object_identifier_004 alter column c9 TYPE TINYINT;
alter table object_identifier_004 alter column c10 TYPE TINYINT;
alter table object_identifier_004 alter column c11 TYPE TINYINT;
alter table object_identifier_004 alter column c12 TYPE TINYINT;
select * from object_identifier_004;
drop table if exists object_identifier_004;
CREATE  TABLE object_identifier_004(
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
insert into object_identifier_004 values (564182,null,null,null,'english','simple',null,'*(integer,integer)',null,'sum(int4)','pg_type','integer');
alter table object_identifier_004 alter column c1 TYPE date;
alter table object_identifier_004 alter column c2 TYPE date;
alter table object_identifier_004 alter column c3 TYPE date;
alter table object_identifier_004 alter column c4 TYPE date;
alter table object_identifier_004 alter column c5 TYPE date;
alter table object_identifier_004 alter column c6 TYPE date;
alter table object_identifier_004 alter column c7 TYPE date;
alter table object_identifier_004 alter column c8 TYPE date;
alter table object_identifier_004 alter column c9 TYPE date;
alter table object_identifier_004 alter column c10 TYPE date;
alter table object_identifier_004 alter column c11 TYPE date;
alter table object_identifier_004 alter column c12 TYPE date;
select * from object_identifier_004;
drop table if exists object_identifier_004;