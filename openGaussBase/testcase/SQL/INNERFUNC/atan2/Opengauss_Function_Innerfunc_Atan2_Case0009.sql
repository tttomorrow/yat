-- @testpoint: 结合group by\order by的使用
drop table if exists atan2_test_01;
create table atan2_test_01(f1 int,f2 bigint,f3 integer,f4 binary_integer,f5 bigint,
                          f6 real,f7 float,f8 binary_double,f9 decimal,f10 number,f11 numeric);
insert into atan2_test_01(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11) values(11,22,33,44,55,11.1,22.2,33.3,44.4,55.5,66.6);
insert into atan2_test_01(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11) values(66,77,88,99,00,'11.1','22.2','33.3','44.4','55.5','66.6');
select cast(atan2(f1,f2) as number(5,2)),cast(atan2(f2,f3) as number(5,2))||2 from atan2_test_01 order by atan2(f1,f2);
select cast(atan2(f2,f3) as number(5,2)),f3 from atan2_test_01 group by atan2(f2,f3),f3 order by 1;
drop table if exists atan2_test_01;
