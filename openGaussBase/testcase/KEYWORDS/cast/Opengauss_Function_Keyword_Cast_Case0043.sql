-- @testpoint: 验证cast函数是否支持distinct关键字
drop table if exists TEST_h CASCADE;
create table TEST_h( riqi date);
insert into TEST_h values(to_date('2018-08-15 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-08-30 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-09-15 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-08-16 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-09-16 17:27:39','yyyy-mm-dd hh24:mi:ss'));
insert into TEST_h values(to_date('2018-08-17 17:27:39','yyyy-mm-dd hh24:mi:ss'));

select distinct cast(riqi as date) from TEST_h order by cast(riqi as date);
drop table if exists TEST_h CASCADE;