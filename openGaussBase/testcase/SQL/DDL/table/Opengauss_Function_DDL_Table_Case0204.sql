-- @testpoint: alter table constraint_clause rename constraint,原限制不存在时合理报错
--正常
drop table if exists al_table_7;
CREATE TABLE al_table_7 (c1 VARCHAR(255),c2 int);
insert into al_table_7 values ('ddd',1);
insert into al_table_7 values ('',2);
insert into al_table_7 values (null,3);
insert into al_table_7 values ('',4);
insert into al_table_7 values (null,5);
ALTER TABLE al_table_7 add constraint al_table_7_1 check(c1 != ''); --error
insert into al_table_7 values ('',7);
insert into al_table_7 values ('','');
ALTER TABLE al_table_7 rename constraint al_table_7_1 to al_table_7_2;  --error
insert into al_table_7 values ('84',7);
insert into al_table_7 values ('',4);
--defult '84'
drop table if exists al_table_7;
CREATE TABLE al_table_7 (c1 VARCHAR(255) default '84',c2 int default 4);
insert into al_table_7 values ('ddd',1);
insert into al_table_7 values ('qwe',2);
insert into al_table_7 values ('qa',3);
insert into al_table_7 values ('q',4);
insert into al_table_7 values ('ed',5);
ALTER TABLE al_table_7 add constraint al_table_7_1 check(c1 != '');
insert into al_table_7 values ('84',7);
insert into al_table_7 values ('',8);
ALTER TABLE al_table_7 rename constraint al_table_7_1 to al_table_7_2;
insert into al_table_7 values ('84',7);
insert into al_table_7 values ('',4);
drop table if exists al_table_7;