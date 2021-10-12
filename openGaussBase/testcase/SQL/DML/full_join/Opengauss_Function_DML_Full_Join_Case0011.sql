-- @testpoint:使用join...on语句，on条件为date和date类型比较，查询成功
-- @modify at: 2020-11-13
--建表
drop table if exists zsharding_tbl;
create table zsharding_tbl(
c_id int, c_int int, c_integer integer, c_bool int, c_boolean int, c_bigint integer,
c_real real, c_double real,
c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_date date, c_datetime date
)
PARTITION BY RANGE (c_integer)
(
partition P_max values less than (maxvalue)
);
--插入数据
INSERT INTO zsharding_tbl VALUES ( 22, 12, 20000, 1, 1, 0, 1, 10, 3000, 13, 0, 'ekb', 'eekbvumxm', 'd', TO_DATE('1995-08-08', 'YYYY-MM-DD'), TO_DATE('2009-11-25', 'YYYY-MM-DD') );
--查询
select t1.c_date,t1.c_date,t2.c_date,t2.c_date from zsharding_tbl t1 full join zsharding_tbl t2 on t1.c_date=t2.c_date order by 1,2,3,4;
--删表
drop table if exists zsharding_tbl;
