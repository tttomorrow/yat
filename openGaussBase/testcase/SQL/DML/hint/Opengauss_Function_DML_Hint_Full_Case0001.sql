-- @testpoint: 索引、视图、约束（违反检查约束，合理报错）
drop view if exists hint_index_000000;
drop table if exists hint_index_00000;
create table hint_index_00000(
c_id int, c_int int, c_integer integer, c_bool bool, c_boolean boolean, c_bigint bigint,
c_real real,

c_decimal decimal(38), c_number number(38), c_numeric numeric(38),
c_char char(50) default null, c_varchar varchar(20), c_varchar2 varchar2(4000),
c_date date
)
partition by range (c_integer)
(
        partition p_max values less than (maxvalue)
);

delete /*+full(hint_index_000000)*/ from hint_index_00000;
delete from hint_index_00000;
insert into hint_index_00000 values ( 22, 12, 20000, 1, 1, 0, 1, 3000, 13, 0, 'ekb', 'eekbvumxm', 'd', to_date('1995-08-08', 'yyyy-mm-dd'));

create index hint_index_00000_idx1 on hint_index_00000(c_integer) local ;
alter table hint_index_00000 add constraint hint_unique1 unique (c_integer,c_id);


create view hint_index_000000 as select c_integer,c_varchar, c_varchar2,c_date from hint_index_00000;

drop table if exists hint1_index_00000;
create table hint1_index_00000(id int not null,c_intger integer,c_char char(10))
partition by range (c_intger)
(
partition p_max values less than (2050)
);
insert into hint1_index_00000 values(1,1000,1000);
insert into hint1_index_00000 values(2,2000,1000);
insert into hint1_index_00000 values(3,2001,null);
insert into hint1_index_00000 values(4,2002,'a');


drop table if exists hint2_index_00000;
create table hint2_index_00000
(customer_id integer,
cust_first_name  varchar(20) not null,
cust_last_name   varchar(20) not null,
credit_limit integer
);
insert into hint2_index_00000 values (1, 'li', 'adjani', 100);
insert into hint2_index_00000 values (2, 'li', 'alexander', 2000);
insert into hint2_index_00000 values (3, 'li', 'altman', 5000);



drop table if exists t_hint;
create table t_hint (fint1 int, fint2 int, fstr1 varchar(128), fstr2 varchar(128));
create index t_hint_idx1 on t_hint(fint1) ;
create index t_hint_idx2 on t_hint(fint2) ;
create index t_hint_idx3 on t_hint(fstr1);
create index t_hint_idx4 on t_hint(fstr2);

insert into t_hint values(1, 2, 'a', 'aa');
insert into t_hint values(2, 4, 'b', 'bb');
insert into t_hint values(3, 6, 'c', 'cc');
insert into t_hint values(4, 8, 'd', 'dd');
insert into t_hint values(5, 10, 'e', 'ee');

drop table if exists t1_hint;

create table t1_hint (fint11 int, fint22 int, fstr11 varchar(128), fstr22 varchar(128));
create index t1_hint_idx1 on t1_hint(fint11);
create index t1_hint_idx2 on t1_hint(fint22);
create index t1_hint_idx3 on t1_hint(fstr11);
create index t1_hint_idx4 on t1_hint(fstr22);

insert into t1_hint values(1, 2, 'a', 'aa');
insert into t1_hint values(2, 4, 'b', 'bb');
insert into t1_hint values(3, 6, 'c', 'cc');
insert into t1_hint values(4, 8, 'd', 'dd');
insert into t1_hint values(5, 10, 'e', 'ee');
drop table if exists t1_hint;