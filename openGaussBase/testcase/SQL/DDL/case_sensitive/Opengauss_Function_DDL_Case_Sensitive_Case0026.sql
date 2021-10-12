--  @testpoint: --创建视图验证视图名大小写
drop table if exists false_2 cascade;
drop table if exists false_3 cascade;
create table false_2 (A int,b int);
create table false_3(A INT,b int);
create or replace view view_2 as select * from FALSE_2;
CREATE OR REPLACE VIEW view_2 as select * from false_2;
create or replace view VIEW_3 as select * from FALSE_3;
create or replace view VIEW_2 as select * from false_3;
create view tabl_1 as select a,B from false_2;
create view tabl_2 as select B from false_3;