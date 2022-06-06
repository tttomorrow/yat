-- @testpoint: list分区键值数量测试，使用values in，部分测试点合理报错
--step1:分区键值数量为64;expect:成功
drop table if exists tb_plugin0010;
create table tb_plugin0010(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values in(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
 21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,
 46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64));

--step2:分区键值数量为65;expect:合理报错
drop table if exists tb_plugin0010_01;
create table tb_plugin0010_01(p_id int,p_name varchar,p_age int)
partition by list(p_id)
(partition part_1 values in(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,
 21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,
 46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65));
 
--step3:清理环境;expect:成功
drop table if exists tb_plugin0010;