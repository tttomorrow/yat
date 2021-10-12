-- @testpoint: 插入无效值,合理报错
-- @modify at: 2020-11-05

DROP TABLE IF EXISTS type_boolean02;
CREATE TABLE type_boolean02 (datev boolean);
insert into type_boolean02 values ('efwqwe');
insert into type_boolean02 values ('哈');
insert into type_boolean02 values ('123.456');
insert into type_boolean02 values ();
select * from type_boolean02;
drop table type_boolean02;