-- @testpoint: 输入参数为decimal类型

drop table if exists bitand_test_03;
create table  bitand_test_03(col_bitand1 integer,col_bitand2 integer,col_bitand3 integer,col_bitand4 integer);
insert into bitand_test_03 values(bitand(5.506,3),bitand(6.4999,3),bitand(6,3.499),bitand(6,2.506));
select * from bitand_test_03;
drop table if exists bitand_test_03;