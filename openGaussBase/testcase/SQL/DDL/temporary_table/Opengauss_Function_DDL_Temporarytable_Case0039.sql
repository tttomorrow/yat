-- @testpoint: 创建临时表，表名中有汉字
-- @modify at: 2020-11-24
drop table if exists global_表_352;
create  temporary table global_表_352(c_id int,c_d_id int not null);
--删表
drop table global_表_352;