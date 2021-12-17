-- @testpoint: alter table在插入数据前后进行添加删除列
drop table if exists table_alter_011;
create table table_alter_011(
c_id int, c_integer integer,
c_real real,c_float float, c_double binary_double,
c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),c_blob blob,
c_date date,c_timestamp timestamp
);

--增加列
alter table table_alter_011 add(c_1 int);
alter table table_alter_011 add(c_2 BLOB default '0101010101111100001110');
alter table table_alter_011 add(c_3 VARCHAR(200));
alter table table_alter_011 add(c_4 CLOB);

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_011' and a.attrelid = c.oid and a.attnum>0;

--删除新增加的列
alter table table_alter_011 drop c_1;
alter table table_alter_011 drop c_2;
alter table table_alter_011 drop c_3;

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_011' and a.attrelid = c.oid and a.attnum>0;

--插入数据
insert into table_alter_011 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
'ywgdghghhgghe',hextoraw('101A1101'),'010101101',date_trunc('hour', timestamp  '2001-02-16 20:38:40'),to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF'),'汉字的环境ihhivhkhv&*&%^&^555'
);

insert into table_alter_011 select * from table_alter_011;
insert into table_alter_011 select * from table_alter_011;
insert into table_alter_011 select * from table_alter_011;

analyze  table_alter_011;

--增加列
alter table table_alter_011 add(c_1 int);
alter table table_alter_011 add(c_2 BLOB default '0101010101111100001110');
alter table table_alter_011 add(c_5 date);
SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_011' and a.attrelid = c.oid and a.attnum>0;

--删除新增加的列
alter table table_alter_011 drop c_1;
alter table table_alter_011 drop c_2;
alter table table_alter_011 drop c_4;
alter table table_alter_011 drop c_5;


SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_011' and a.attrelid = c.oid and a.attnum>0;
drop table if exists table_alter_011;