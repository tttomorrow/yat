-- @testpoint: having条件
drop table if exists abs_test_03;
create table abs_test_03(a int,b int);
insert into abs_test_03 values(5,10);
insert into abs_test_03 values(1,9);
insert into abs_test_03 values(2,10);
select sum(a),b from abs_test_03 group by b having abs(b)=10 order by b;
drop table if exists abs_test_03;