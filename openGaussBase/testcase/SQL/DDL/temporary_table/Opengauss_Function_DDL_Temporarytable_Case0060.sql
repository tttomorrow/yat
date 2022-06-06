-- @testpoint: 子查询为嵌套查询，与union结合并且引用主表的列
-- @modify at: 2020-11-24
--建表
drop table if exists temp_table_060;
create global TEMPORARY table temp_table_060(
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
)on commit preserve rows;
--插入数据
insert into temp_table_060 values(1,0,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','jjj','pokj99',
'ywgdghghhgghe',HEXTORAW('DEADBEEF'),'010101101','2019-01-03 14:14:12',to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF'));
insert into temp_table_060 values(2,1,3.14,1.0002,3.55555,5,7887.656,0,0.111111,3.1415926,'dghg','saga','pokj99',
'ywgdghghhgghe',HEXTORAW('DEADBEEF'),'010101101','2019-01-03 14:14:12',to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF'));
--修改数据
update temp_table_060 t1 set (c_integer,c_varchar) = (select distinct c1,c2 from (select c_integer c1,c_varchar c2 from temp_table_060 union
select c_integer c1,c_varchar c2 from temp_table_060 where t1.c_integer=c_integer limit 1));
--查询
select c_integer,c_varchar from temp_table_060 order by 1;
--删表
drop table temp_table_060;




