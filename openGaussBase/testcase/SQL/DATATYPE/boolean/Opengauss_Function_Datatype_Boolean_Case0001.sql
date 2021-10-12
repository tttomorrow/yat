-- @testpoint: 插入有效值
-- @modify at: 2020-11-05


DROP TABLE IF EXISTS type_boolean01;
CREATE TABLE type_boolean01 (datev boolean);

--有效真值
insert into type_boolean01 values (true);
insert into type_boolean01 values ('true');
insert into type_boolean01 values (TRUE);
insert into type_boolean01 values ('TRUE');
insert into type_boolean01 values ('t');
insert into type_boolean01 values ('y');
insert into type_boolean01 values ('yes');
insert into type_boolean01 values ('1');
insert into type_boolean01 values (1);
insert into type_boolean01 values (-1);


--有效假值
insert into type_boolean01 values (false);
insert into type_boolean01 values ('false');
insert into type_boolean01 values (FALSE);
insert into type_boolean01 values ('FALSE');
insert into type_boolean01 values ('f');
insert into type_boolean01 values ('n');
insert into type_boolean01 values ('no');
insert into type_boolean01 values ('0');
insert into type_boolean01 values (0);


select * from type_boolean01;
drop table type_boolean01;
