-- @testpoint: create table时复制有多列约束和不同字段类型的表结构
drop table if exists test;
drop table if exists tb_1;
create table test(
id              NUMBER(7) CONSTRAINT s_longtext_id_nn NOT NULL,
use_filename    VARCHAR2(20) default 'upgrade',
filename        VARCHAR2(255) default null,
text            VARCHAR2(2000)
);
create table tb_1 as select * from test;
drop table if exists test;
drop table if exists tb_1;
