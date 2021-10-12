--  @testpoint:alter验证表名大小写敏感
ALTER TABLE false_1 drop v cascade;
alter table FALSE_1 ADD V INT;
ALTER TABLE false_1 add v int;
alter table FALSE_1 MODIFY A CHAR(10);
alter table false_1 MODIFY a CHAR(10);