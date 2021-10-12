-- @testpoint: update语句中使用自定义函数的同义词
--建表1
drop table if exists SYN_TAB_001 cascade;
create table SYN_TAB_001
(
	id int,
    c_bigint bigint,
    c_bool boolean,
    c_number number(38, 0),
    c_dec decimal(38, 0),
    c_float float,
    c_double DOUBLE PRECISION,
    c_real real,
    c_char char(128),
    c_varchar varchar(512),
    c_varchar2 varchar2(512),
    c_date date,
    c_timestamp timestamp
);
--插入数据
begin
	for i in 1..500 loop
		insert into SYN_TAB_001 values(i,i+1,cast(cast(mod(i,2) as int)as boolean),i+2,i+3,i+4,i+5,i+6,'a'||i,'aa'||i,'中国'||i,'2019-06-27','2019-06-27 10:56:48');
	end loop;
end;
/
--创建函数的同义词
drop synonym if exists SYN_TAB_SYN_001;
create or replace  synonym  SYN_TAB_SYN_001 for SYN_TAB_001;
--建表2
drop table if exists SYN_TAB_002;
create table SYN_TAB_002
(
 new_id int,
 c_uint bigint,
 c_clob clob,
 c_blob blob
);
--插入数据
begin
	for i in 1..1000 loop
	end loop;
end;
/
--创建同义词
drop synonym if exists SYN_TAB_SYN_002;
create or replace  synonym  SYN_TAB_SYN_002 for SYN_TAB_002;
--建表3
drop table if exists SYN_TAB_003;
create table SYN_TAB_003
(
	f_id int,
	f_int integer[],
	f_varchar varchar(30)[]
);
--插入数据
begin
	for i in 1..1000 loop
		insert into SYN_TAB_003 values (i,array[1,2,3,4,5],array['a','b','c','d','e']);
	end loop;
end;
/
--创建同义词
drop synonym if exists SYN_TAB_SYN_003;
create or replace  synonym  SYN_TAB_SYN_003 for SYN_TAB_003;
--创建函数
drop function if exists SYN_FUN_001(a varchar) cascade;
create or replace function SYN_FUN_001 (a varchar) return int
as
b int;
begin
	b:=length(a);
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_001;
create or replace  synonym  SYN_FUN_SYN_001 for SYN_FUN_001;
--创建函数
drop function if exists SYN_FUN_002(a varchar) cascade;
create or replace function SYN_FUN_002 (a varchar) return varchar
as
b varchar(1024);
begin
	b:=a||a;
	return b;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_002;
create or replace  synonym  SYN_FUN_SYN_002 for SYN_FUN_002;
--创建函数
drop function if exists SYN_FUN_003(a number,str varchar) cascade;
create or replace function SYN_FUN_003(a number,str varchar) return varchar
as
	cur sys_refcursor;
	var varchar(1024);
	new_var varchar(1024):=str;
begin
	open cur for select str from sys_dummy;
	for i in 1..a loop
		fetch cur into var;
		exit when cur%notfound;
		new_var:=new_var||var;
	end loop;
	return new_var;
end;
/
--创建同义词
drop synonym if exists SYN_FUN_SYN_003;
create or replace  synonym  SYN_FUN_SYN_003 for SYN_FUN_003;
--修改表1的同义词数据
update SYN_TAB_SYN_001 set c_varchar= SYN_FUN_SYN_002(c_varchar)
where id in
(select distinct SYN_TAB_SYN_003.f_id
from SYN_TAB_SYN_001
join SYN_TAB_SYN_002 on SYN_TAB_SYN_001.id=SYN_TAB_SYN_002.new_id
join SYN_TAB_SYN_003 on SYN_TAB_SYN_002.new_id=SYN_TAB_SYN_003.f_id and SYN_FUN_SYN_001(SYN_FUN_SYN_002(c_varchar))=SYN_FUN_SYN_001(c_varchar2)*2);
--清理环境
drop table if exists SYN_TAB_001 cascade;
drop table if exists SYN_TAB_002 cascade;
drop table if exists SYN_TAB_003 cascade;
drop function if exists SYN_FUN_001(a varchar) cascade;
drop function if exists SYN_FUN_002(a varchar) cascade;
drop function if exists SYN_FUN_003(a number,str varchar) cascade;
drop synonym if exists SYN_FUN_SYN_001;
drop synonym if exists SYN_FUN_SYN_002;
drop synonym if exists SYN_FUN_SYN_003;
drop synonym if exists SYN_TAB_SYN_001;
drop synonym if exists SYN_TAB_SYN_002;
drop synonym if exists SYN_TAB_SYN_003;