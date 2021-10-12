-- @testpoint: insert into 
drop table if exists tb1;
create table tb1( 
COL_1 bigint, 
COL_2 time without time zone, 
COL_3 bool,
COL_4 decimal,
COL_5 text,
COL_6 varchar,
COL_7 char(50));

insert into tb1 values(CONCAT_WS(3,'11','22'),null,null,null,null,null,null);
insert into tb1 values(null,to_timestamp(CONCAT_WS(':','29','Jan','1999')),null,null,null,null,null);
insert into tb1 values(null,null,CONCAT_WS('1','1')>'1',null,null,null,null);
insert into tb1 values(null,null,null,CONCAT_WS('.','11','2987'),null,null,null);
insert into tb1 values(null,null,null,null,CONCAT_WS('great','oh ',' job'),null,null);
insert into tb1 values(null,null,null,null,null,CONCAT_WS('A','F','E'),null);
insert into tb1 values(null,null,null,null,null,null,CONCAT_WS(3,'11','22'));
select * from tb1;
drop table if exists tb1;
