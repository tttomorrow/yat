-- @testpoint: 创建约束，结合abs函数，合理报错
-- @modify at: 2020-11-23
--建表并指定约束，报错
drop table if exists test_unique_constraint025;
create table test_unique_constraint025 (id_p int not null, lastname varchar(255) not null, firstname varchar(255),address varchar(255), city varchar(255),constraint uc_personid unique (abs(id_p)));