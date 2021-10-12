--  @testpoint: --alter drop 验证字段名大小写敏感
alter table false_1 drop column B;
alter table FALSE_1 ADD b INT;
alter table false_1 drop column b;