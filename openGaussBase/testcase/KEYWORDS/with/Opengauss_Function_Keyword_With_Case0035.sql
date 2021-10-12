-- @testpoint: 关键字with，正常执行insert into with语句


drop table if exists with_test_01;
drop table if exists with_test_02;
create table with_test_01(a int,b char(2));
create table with_test_02(a int,b char(2));

insert into with_test_02 values(2,6);

insert into with_test_01 with a as (select a from with_test_02),b as (select b from with_test_02) select a.a,b.b from a,b order by 1,2;
insert into with_test_01 with b as (select b from with_test_02) select b.b,b.b from b;

select * from with_test_01 order by 1,2;
drop table if exists with_test_01;
drop table if exists with_test_02;