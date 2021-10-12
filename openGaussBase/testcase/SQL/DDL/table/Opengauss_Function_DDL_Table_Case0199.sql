-- @testpoint: alter table在default NULL default '' default 普通值 时core
-- @testpoint: alter table references_clause (default null)
drop table if exists al_table_1;
drop table if exists al_table_2;
CREATE TABLE al_table_1 (c1 VARCHAR(255) default null,c2 int default null);
insert into al_table_1 values ('ddd',1);
insert into al_table_1 values ('',2);
insert into al_table_1 values (null,3);

ALTER TABLE al_table_1 add constraint pk_al_table_1_1 PRIMARY KEY(c2);
drop table if exists al_table_2;
CREATE TABLE al_table_2(c1 VARCHAR(255) default null,c2 int default null);
insert into al_table_2 values ('ddd',1);
insert into al_table_2 values ('',2);
insert into al_table_2 values (null,3);

ALTER TABLE al_table_2 add  constraint  UN_C2 UNIQUE(c2) ;
drop table if exists al_table_2;
drop table if exists al_table_1;
