-- @testpoint: 插入空值
-- @modified at: 2020-11-16

drop table if exists special_char_05;
CREATE  TABLE special_char_05 (id int,name "char");
insert into special_char_05 values (1,'');
insert into special_char_05 values (1,null);
select * from special_char_05;
drop table special_char_05;