-- @testpoint: 12.insert into语句中使用
drop table if exists test_tb_addm;
create  table test_tb_addm
(
id integer,
month date
);
create index test_tb_addm_index on test_tb_addm(month);
insert into test_tb_addm values(1,'2019-03-01');
insert into test_tb_addm values(2,ADD_MONTHS('2019-03-01',2));
commit;
drop table if exists test_tb_addm;