-- @testpoint: 创建表空间同义词:创建成功，使用时，合理报错
--创建用户和表空间
drop user if exists syn001_a cascade;
CREATE user syn001_a IDENTIFIED BY 'Test@123';
drop TABLESPACE if exists ds_location1;
CREATE TABLESPACE ds_location1 OWNER syn001_a RELATIVE LOCATION 'tablespace/tablespace_2adsvc';
--创建同义词：无效
drop SYNONYM if exists syn_table_space;
create synonym syn_table_space for ds_location1;
--查询
select * from syn_table_space;
--清理环境
drop TABLESPACE if exists ds_location1;
drop user syn001_a cascade;
drop SYNONYM if exists syn_table_space;