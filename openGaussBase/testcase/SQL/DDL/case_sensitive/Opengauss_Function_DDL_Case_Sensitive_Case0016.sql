--  @testpoint: --函数验证字段名大小写
insert into false_1 values(2,5);
select length(a) from false_1 where a=2;
insert into false_1 values(2,657);
select length(A) from false_1 where a=2;
select length(B) from false_1 where a=2;
select length(b) from false_1 where a=2;