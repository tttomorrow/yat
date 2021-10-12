--  @testpoint:opengauss关键字owned(非保留)，修改序列归属列

Create user ceshi identified by 'Xiaxia@123';
Grant all privileges to ceshi;
CREATE SEQUENCE serial_1 START 102;
ALTER SEQUENCE  IF EXISTS  serial_1 OWNER TO ceshi;
DROP SEQUENCE serial_1 cascade;
drop user ceshi;
