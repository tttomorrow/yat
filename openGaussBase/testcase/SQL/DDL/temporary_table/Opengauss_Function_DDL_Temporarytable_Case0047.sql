-- @testpoint: 创建表名超过63位的临时表，存在同名的表，合理报错
--建表1
drop table if exists qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnbqwewr;
create  temporary table qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnbqwewr(a int);
--创建表,表名使用表1中截取的前63位,报错
create  temporary table qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnb(a int);
--删表
drop table qwertyuiopqasdfghjklzxcvbnmpolkijuyhtgfrdppoiuytrqwelkijhgfdmnbqwewr;



