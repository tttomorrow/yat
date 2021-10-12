--  @testpoint:opengauss关键字owner(非保留)，修改模式拥有者
CREATE SCHEMA ds_1;
CREATE USER jack_1 PASSWORD 'Bigdata@123';
ALTER SCHEMA ds_1 OWNER TO jack_1;
DROP SCHEMA ds_1;
DROP USER jack_1;
