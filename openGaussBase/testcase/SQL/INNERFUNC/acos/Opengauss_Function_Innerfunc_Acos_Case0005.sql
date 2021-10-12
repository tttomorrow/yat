--  @testpoint:having的使用

drop table if exists acos_test_02;
create table acos_test_02(a int,b int);
insert into acos_test_02 values(5,1);
insert into acos_test_02 values(1,-1);
insert into acos_test_02 values(2,1);

select sum(a),b from acos_test_02 group by b having acos(b)=0 order by b;
drop table if exists acos_test_02;
