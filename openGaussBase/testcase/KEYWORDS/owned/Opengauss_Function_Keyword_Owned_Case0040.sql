--  @testpoint:opengauss关键字owned(非保留)，修改数据库对象属主


Create user ceshi1 identified by 'Xiaxia@123';
Grant all privileges to ceshi1;
DROP OWNED BY  ceshi1;

Create user ceshi2 identified by 'Xiaxia@123';
Grant all privileges to ceshi2;
DROP OWNED BY  ceshi2;
REASSIGN OWNED BY ceshi1 TO ceshi2;
drop user ceshi1;
drop user ceshi2;