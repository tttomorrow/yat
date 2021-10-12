-- @testpoint: 修改所有列的数据类型为clob
-- @modify at: 2020-11-23
--创建全局临时表
drop table if exists temp_table_alter_007;
create global temporary table temp_table_alter_007(
c_id int,
c_integer integer,
c_real real,
c_float float,
c_double binary_double,
c_decimal decimal(38),
c_number number(38),
c_number1 number,
c_number2 number(20,10),
c_numeric numeric(38),
c_char char(50) default null,
c_varchar varchar(20),
c_varchar2 varchar2(4000),
c_clob clob,
c_raw raw(20),
c_blob blob,
c_date date,
c_timestamp timestamp
);
--修改数据类型
alter table temp_table_alter_007 modify(c_id clob,c_integer clob,c_real clob,c_float clob,c_double clob,c_decimal clob,c_number clob,c_number1 clob,c_number2 clob,c_numeric clob,
c_char clob,c_varchar clob,c_varchar2 clob,c_clob clob,c_raw clob,c_timestamp clob,c_blob clob);
--插入数据
insert into temp_table_alter_007 (c_double,c_raw) values(10.258,hextoraw('deadbeef'));
insert into temp_table_alter_007 (c_double,c_raw) values(1589.521,'测试');
--查询表查询表信息
select * from temp_table_alter_007;
--删表
drop table temp_table_alter_007;