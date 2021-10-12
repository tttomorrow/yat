-- @testpoint: 输入为有效值的测试

drop table if exists bitand_test_01;
create table  bitand_test_01(col_bitand1 integer,col_bitand2 integer,col_bitand3 integer);
insert into bitand_test_01 values(bitand(6,3),bitand(-1,1),bitand(-1,-1));
select * from bitand_test_01;
drop table if exists bitand_test_01;