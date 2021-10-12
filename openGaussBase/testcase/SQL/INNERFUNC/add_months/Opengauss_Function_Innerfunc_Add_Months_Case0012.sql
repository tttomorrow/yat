-- @testpoint: 13.UPDATE语句中使用
drop table if exists test_tb_addm;
create  table test_tb_addm
(
id integer,
month date
);
create index test_tb_addm_index on test_tb_addm(month);
insert into test_tb_addm values(2,ADD_MONTHS('2019-03-01',2));
update test_tb_addm  set month=add_months(month,1) where id =2;
commit;
drop table if exists test_tb_addm;