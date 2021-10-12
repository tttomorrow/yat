-- @testpoint: 建表未指定列名,合理报错
drop table if exists qaz;
create table qaz(varchar not null defualt 'aaaaaaaaaaaaa');
drop table qaz;