-- @testpoint: 创建临时表，表名长度为63
-- @modify at: 2020-11-24
--建表，成功
drop table if exists qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnb;
create  temporary table qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnb(a int);
--查询
select * from qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnb;
--删表
drop table qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnb;


