-- @testpoint: analyze收集表33列数据,合理报错
--设置参数default_statistics_target为负数
set default_statistics_target to -100;
--建表，列数超过32列
drop table if exists test_1;
create table test_1 (c_id int,c_name varchar(20),c_age int,c_sex varchar(20),c_height int,c_color varchar(20),
c_id1 int,c_name1 varchar(20),c_age1 int,c_sex1 varchar(20),c_height1 int,c_color1 varchar(20),
c_id2 int,c_name2 varchar(20),c_age2 int,c_sex2 varchar(20),c_height2 int,c_color2 varchar(20),
c_id3 int,c_name3 varchar(20),c_age3 int,c_sex3 varchar(20),c_height3 int,c_color3 varchar(20),
c_id4 int,c_name4 varchar(20),c_age4 int,c_sex4 varchar(20),c_height4 int,c_color4 varchar(20),
c_id5 int,c_name5 varchar(20),c_age5 int,c_sex5 varchar(20),c_height5 int,c_color5 varchar(20),
c_id6 int,c_name6 varchar(20),c_age6 int,c_sex6 varchar(20),c_height6 int,c_color6 varchar(20)
);
--使用analyze，分析表的33列，合理报错ERROR:  Multi-column statistic supports at most 32 columns
analyze test_1((c_id1,c_name1,c_age1,c_sex1,c_height1,c_color1,
c_id2,c_name2,c_age2,c_sex2,c_height2,c_color2,
c_id3,c_name3,c_age3,c_sex3,c_height3,c_color3,
c_id4,c_name4,c_age4,c_sex4,c_height4,c_color4,
c_id5,c_name5,c_age5,c_sex5,c_height5,c_color5,
c_id6,c_name6,c_age6,c_sex6));
--删表
drop table test_1;
--恢复参数默认值
set default_statistics_target to 100;
show default_statistics_target ;