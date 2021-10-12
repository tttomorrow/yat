--  @testpoint: --insert子查询语句验证表名大小写
insert into false_1 select * from False_1;
insert into falsE_1 select * from False_1;
insert into falsE_1 values(8);
insert into false_1 select * from falsE_1;
select * from false_1;
insert into false_1 select * from false_1;