--  @testpoint: --select 验证字段名大小写不敏感
select A from false_1;
select a from false_1;
select b from false_1;
select B from false_1;
select a,A,b from false_1;
select a,B from false_1;
