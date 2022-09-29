-- @testpoint: 不同表类型，建表指定engine参数
--testpoint1:
--step1:创建一种复合类型;expect:成功
drop type if exists ty_grammar0001 cascade;
create type ty_grammar0001 as (a int, b text);
--step2:创建普通行存表，engine参数值为加引号的字符串;expect:成功
drop table if exists tb_b_grammar_0001;
create table tb_b_grammar_0001(a text(10),b tinytext,c mediumtext,d longtext, e ty_grammar0001) engine ='myisam';
--step3:插入数据;expect:成功
insert tb_b_grammar_0001 value('测试1','测试2$','测试3','测试acv', (827,'复合类型'));

--testpoint2:
--step1:创建列存表，engine参数值为不加引号的字符串;expect:成功
drop table if exists tb_b_grammar_0001_01;
create table tb_b_grammar_0001_01(a int) with(orientation=column) engine = innodb ;

--testpoint3:
--step1:创建unlogged表,复制已有表数据;expect:成功
drop table if exists tb_b_grammar_0001_02;
create unlogged table tb_b_grammar_0001_02 engine = 'case0001' as select * from tb_b_grammar_0001;

--testpoint4:
--step1:创建全局临时表指定engine参数;expect:成功
drop table if exists tb_b_grammar_0001_03;
create global temp table tb_b_grammar_0001_03(a text(10),b tinytext,c mediumtext,d longtext)engine ='全局临时表';
--step2:创建本地临时表指定engine参数;expect:成功
drop table if exists tb_b_grammar_0001_03;
create temporary  table tb_b_grammar_0001_03(a text(10),b tinytext,c mediumtext,d longtext)engine ='本地临时表';

--testpoint5:
--step1:创建ustore表指定engine参数;expect:成功
drop table if exists tb_b_grammar_0001_04;
create temp table tb_b_grammar_0001_04(a text(10),b tinytext,c mediumtext,d longtext)with (storage_type=ustore)engine ='case0001';

--step1:清理环境;expect:成功
drop table if exists tb_b_grammar_0001;
drop table if exists tb_b_grammar_0001_01;
drop table if exists tb_b_grammar_0001_02;
drop table if exists tb_b_grammar_0001_03;
drop table if exists tb_b_grammar_0001_04;
drop type ty_grammar0001;



