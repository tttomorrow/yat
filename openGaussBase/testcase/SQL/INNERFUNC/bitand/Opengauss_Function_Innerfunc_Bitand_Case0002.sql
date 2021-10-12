-- @testpoint: 输入参数为0

drop table if exists bitand_test_02;
create table  bitand_test_02(col_bitand1 integer,col_bitand2 integer,col_bitand3 integer);
insert into bitand_test_02 values(bitand(0,3),bitand(-1,0),bitand(-1,0));
select * from bitand_test_02;
drop table if exists bitand_test_02;