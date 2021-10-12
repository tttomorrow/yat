--  @testpoint:opengauss关键字owned(非保留)，删除数据库角色所拥有得数据库对象

Create user ceshi identified by 'Xiaxia@123';
Grant all privileges to ceshi;
DROP OWNED BY  ceshi;
drop user ceshi;





