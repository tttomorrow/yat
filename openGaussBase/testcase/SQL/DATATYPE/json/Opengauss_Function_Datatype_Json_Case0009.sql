-- @testpoint: 插入特殊字符,合理报错

drop table if exists test_json_09;
create table test_json_09 (id json);
insert into test_json_09 values ('……（*');
insert into test_json_09 values ('{"@":@,"#":#,"$":$}');
drop table test_json_09;