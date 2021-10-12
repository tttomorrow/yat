-- @testpoint: 插入非法字符

drop table if exists special_char_07;
CREATE  TABLE special_char_07 (id "char");
insert into special_char_07 values ('@#%…（/&*……*');
select * from special_char_07;
drop table special_char_07;