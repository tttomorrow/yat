-- @testpoint: 相对时间间隔类型reltime,插入无效值，合理报错

drop table if exists reltime02;
create table reltime02 (name reltime);
insert into reltime02 values ('faefae');
insert into reltime02 values ('#￥%……&*');
drop table reltime02;