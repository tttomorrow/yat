-- @testpoint: insert into语句中使用
drop table if exists test_nullif_003;
create table test_nullif_003(COL_01 char(20));
insert into test_nullif_003 values (nullif(4,6));
insert into test_nullif_003 values (nullif('lalalala','天空'));
insert into test_nullif_003 values (nullif('天空','lalalala'));
insert into test_nullif_003 values (nullif(cast('199044' as number),192));
select COL_01 from test_nullif_003 order by 1;
drop table test_nullif_003;