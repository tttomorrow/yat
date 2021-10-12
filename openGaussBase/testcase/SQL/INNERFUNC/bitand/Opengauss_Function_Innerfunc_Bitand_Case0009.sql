--  @testpoint:输入为二进制（合理报错）

drop table if exists bitand_test_06;
create table  bitand_test_06(col_bitand1 integer,col_bitand2 integer);
insert into bitand_test_06 values(bitand('11010011','10101010'),bitand('00110011','10101010'));
select * from bitand_test_06;
drop table if exists bitand_test_06;
