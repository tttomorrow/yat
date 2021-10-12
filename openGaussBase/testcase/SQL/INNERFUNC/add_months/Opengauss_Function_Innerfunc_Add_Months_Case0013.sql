-- @testpoint: 14.delete的使用
drop table if exists test_tb_addm;
create  table test_tb_addm
(
id integer,
month date
);
create index test_tb_addm_index on test_tb_addm(month);
insert into test_tb_addm values(2,ADD_MONTHS('2019-03-01',2));
delete from  test_tb_addm where add_months(month,1)='2019-04-01 00:00:00';
commit;
drop table if exists test_tb_addm;
