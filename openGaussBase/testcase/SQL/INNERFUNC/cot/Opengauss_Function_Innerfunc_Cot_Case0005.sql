-- @testpoint: 与distinct、order by结合使用测试

drop table if exists cos_test_01;
create table cos_test_01(a int,b int);
insert into cos_test_01 values(0,1);
insert into cos_test_01 values(1,-1);
insert into cos_test_01 values(2,1);

select b from cos_test_01 order by abs(cot(a));
select distinct cot(b) from cos_test_01 order by cot(b);
drop table if exists cos_test_01;
