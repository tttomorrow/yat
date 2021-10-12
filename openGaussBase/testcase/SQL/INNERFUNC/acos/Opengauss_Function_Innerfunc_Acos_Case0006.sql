--  @testpoint:部分关键字的结合使用

drop table if exists acos_test_03;
create table acos_test_03(a decimal(10,2));
insert into acos_test_03 values(1);
insert into acos_test_03 values(-1);
insert into acos_test_03 values(0.5);
insert into acos_test_03 values(0.8);

select acos(a) t1 from acos_test_03 union all select acos(a) t1 from acos_test_03 order by t1;
select acos(a) t1 from acos_test_03 union select acos(a) t1 from acos_test_03 order by t1;
select count(acos(a)) from acos_test_03;
drop table if exists acos_test_03;
