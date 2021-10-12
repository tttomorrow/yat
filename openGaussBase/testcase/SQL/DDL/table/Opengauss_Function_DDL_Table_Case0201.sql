-- @testpoint: alter table constraint_clause设置主键后给限制重命名
--正常
drop table if exists al_table_5;
CREATE TABLE al_table_5 (c1 VARCHAR(255),c2 int);
insert into al_table_5 values ('ddd',1);
insert into al_table_5 values ('',2);
insert into al_table_5 values (null,3);
insert into al_table_5 values ('',4);
insert into al_table_5 values (null,5);

ALTER TABLE al_table_5 add constraint con_al_table_5_1 PRIMARY KEY(c2);
insert into al_table_5 values (null,7);
insert into al_table_5 values ('',8);
ALTER TABLE al_table_5 rename constraint con_al_table_5_1 to con_al_table_5_3;
--defult ''
drop table if exists al_table_5;
CREATE TABLE al_table_5 (c1 VARCHAR(255) default '',c2 int default '');
insert into al_table_5 values ('ddd',1);
insert into al_table_5 values ('',2);
insert into al_table_5 values (null,3);
insert into al_table_5 values ('',4);
insert into al_table_5 values (null,5);

ALTER TABLE al_table_5 add constraint con_al_table_5_1 PRIMARY KEY(c2);
insert into al_table_5 values (null,7);
insert into al_table_5 values ('',8);
ALTER TABLE al_table_5 rename constraint con_al_table_5_1 to con_al_table_5_3;
drop table if exists al_table_5;



