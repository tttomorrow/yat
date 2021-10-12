--  @testpoint:将数据库postgres的连接权限授权给用户joe

drop user if EXISTS jonyi;
CREATE USER jonyi PASSWORD 'Bigdata@123';
GRANT create,connect on database postgres TO jonyi;
drop user jonyi cascade;