-- @testpoint: 数据类型的测试
DROP TABLE IF EXISTS listagg_tab1;
CREATE TABLE listagg_tab1(
     COL_1 integer,
     COL_2 bigint,
     COL_3 double precision,
     COL_4 decimal(12,6),
     COL_5 boolean,
     COL_6 char(30),
     COL_7 varchar2(50),
     COL_8 varchar(30),
     COL_9 INTERVAL DAY(3) TO SECOND (4),
     COL_10 TIMESTAMP,
     COL_11 date,
     COL_13 TIMESTAMP WITHOUT TIME ZONE,
     COL_14 blob,
     COL_15 clob,
     COL_16 int[]);
--创建序列
drop sequence if exists rank_datatype_seq;
create sequence rank_datatype_seq increment by 1 start with 10;

--清空数据
truncate table listagg_tab1;

--插入数据
 
insert into listagg_tab1 values(1,
rank_datatype_seq.nextval, 
1+445.255,
98*0.99, 
true,
lpad('abc','6','@'),
lpad('abc','5','b'),
rpad('abc','6','e'),
(INTERVAL '4 5:12:10.222' DAY TO SECOND(3)),
to_timestamp('2019-01-03 14:58:54.000000','YYYY-MM-DD HH24:MI:SS.FFFFFF'),
date '12-10-2010',
'2010-12-12',
empty_blob(),
rpad('abc','9','a@123&^%djgk'),
'{32,535,5645645,6767,76,67,56,48,979,978,7}');
--清理环境
DROP TABLE IF EXISTS listagg_tab1;
drop sequence if exists rank_datatype_seq;