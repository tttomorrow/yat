--  @testpoint: --update验证表名大小写敏感
insert into false_1(a) values(6);
insert into false_1(A) values(90);
update FALSE_1 SET a=9 where A is null;
update false_1 set a=9 where a=6;