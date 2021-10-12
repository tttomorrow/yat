-- @testpoint: alter table修改列类型为其不能转换的类型，合理报错


drop table if exists table_alter_010;
create table table_alter_010(
c_id int, c_integer integer,
c_real real,c_float float, c_double binary_double,
c_decimal decimal(38), c_number number(38),c_number1 number,c_number2 number(20,10),c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),c_blob blob,
c_date date,c_timestamp timestamp
);

alter table table_alter_010 modify(c_integer char(60));
alter table table_alter_010 modify(c_float int);
alter table table_alter_010 modify(c_number char(60));
alter table table_alter_010 modify(c_date real);

insert into table_alter_010 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
);

--修改成同类型
alter table table_alter_010 modify(c_integer char(60));
alter table table_alter_010 modify(c_float int);
alter table table_alter_010 modify(c_number char(100));
alter table table_alter_010 modify(c_date real);

insert into table_alter_010 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
);
--修改成其他类型
alter table table_alter_010 modify(c_integer int);
alter table table_alter_010 modify(c_float char(20));
alter table table_alter_010 modify(c_number char(60));
alter table table_alter_010 modify(c_date date);

insert into table_alter_010 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
);

SELECT col_description(a.attrelid,a.attnum) as comment,format_type(a.atttypid,a.atttypmod) as type,a.attname as name, a.attnotnull as notnull
FROM pg_class as c,pg_attribute as a
where c.relname = 'table_alter_010' and a.attrelid = c.oid and a.attnum>0;
drop table if exists table_alter_010;
