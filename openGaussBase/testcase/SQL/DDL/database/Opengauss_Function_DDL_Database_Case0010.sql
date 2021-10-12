-- @testpoint: 删除数据库,合理报错

create database test0010;
drop database test0010;
drop database test0010;
drop database if exists test0010;
drop database postgres;
drop database TEMPLATE0;
drop database TEMPLATE1;
create database test0010;
start transaction;
drop database if exists test0010;
end;

--tearDown
drop database if exists test0010;

