--  @testpoint: order by 条件，验证字段大小写
select * from false_1 order by B;
select * from false_1 order by b;
select * from false_1 order by a;
select * from false_1 order by A;