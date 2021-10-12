-- @testpoint: 结合delete and where条件的使用

drop table if exists bitand_test_05;
CREATE TABLE  bitand_test_05(col_bitand1 integer,col_bitand2 integer);
insert into bitand_test_05 values(bitand(6,3),bitand(-1,1));
insert into bitand_test_05 values(bitand(6,0),bitand(3,2));
select * from bitand_test_05 where col_bitand1>=bitand(6,0) order by col_bitand1,col_bitand2;
delete from bitand_test_05 WHERE col_bitand1>bitand(6,0);
select * from bitand_test_05 order by col_bitand1,col_bitand2;
drop table if exists bitand_test_05;