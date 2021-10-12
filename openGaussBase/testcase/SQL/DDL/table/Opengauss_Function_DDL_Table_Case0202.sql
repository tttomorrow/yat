-- @testpoint: 设置主键后给约束重命名
--正常
drop table if exists al_table_6;
CREATE TABLE al_table_6 (c1 VARCHAR(255),c2 int);
insert into al_table_6 values ('ddd',1);
insert into al_table_6 values ('',2);
insert into al_table_6 values (null,3);
insert into al_table_6 values ('',4);
insert into al_table_6 values (null,5);
ALTER TABLE al_table_6 add constraint con_al_table_6_1 PRIMARY KEY(c2);
insert into al_table_6 values (null,7);
insert into al_table_6 values ('',8);
ALTER TABLE al_table_6 rename constraint con_al_table_6_1 to con_al_table_6_3;
--defult null
drop table if exists al_table_6;
CREATE TABLE al_table_6 (c1 VARCHAR(255) default null,c2 int default null);
insert into al_table_6 values ('ddd',1);
insert into al_table_6 values ('',2);
insert into al_table_6 values (null,3);
insert into al_table_6 values ('',4);
insert into al_table_6 values (null,5);

ALTER TABLE al_table_6 add constraint con_al_table_6_1 PRIMARY KEY(c2);
insert into al_table_6 values (null,7);
insert into al_table_6 values ('',8);
ALTER TABLE al_table_6 rename constraint con_al_table_6_1 to con_al_table_6_3;
drop table if exists al_table_6;



