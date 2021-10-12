--  @testpoint: --delete验证表名大小写敏感
delete from FALSE_1;
delete from false_1;
SELECT * FROM falsE_1;
select * from false_1;
delete from falsE_1;
SELECT * FROM falsE_1;