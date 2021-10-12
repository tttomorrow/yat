-- @testpoint: covar_samp函数入参为算术运算符表达式
drop table if exists T_VAR_POP_SAMP_VARIANCE01;
CREATE TABLE  T_VAR_POP_SAMP_VARIANCE01(
     COL_1 integer,
     COL_2 number(19,0), 
     COL_3 number(10,6));
insert into T_VAR_POP_SAMP_VARIANCE01 values(7,312.245,7+445.255);
insert into T_VAR_POP_SAMP_VARIANCE01 values(5,112.245,7+443.255);
select covar_samp(COL_2/COL_3+COL_3,COL_2/COL_2+COL_3) from T_VAR_POP_SAMP_VARIANCE01 order by 1;
select covar_samp(-(-COL_1*-COL_2-mod(COL_2,COL_3)),-(-COL_1*-COL_2-mod(COL_2,COL_3))) from T_VAR_POP_SAMP_VARIANCE01 order by 1;
select -covar_samp((-COL_1*-COL_2-mod(COL_2,COL_3)),(-COL_1*-COL_2-mod(COL_2,COL_3))) from T_VAR_POP_SAMP_VARIANCE01 order by 1;
select covar_samp(COL_2/COL_3/COL_1/COL_3/COL_2/COL_1/COL_3/COL_3/COL_1,COL_1/COL_3/COL_2/COL_1/COL_3/COL_3/COL_1/COL_3/COL_2/COL_1/COL_3) from T_VAR_POP_SAMP_VARIANCE01 order by 1;
--oracle报错，gaussdb能正常运算
select covar_samp(COL_1+-COL_2-COL_2%COL_3,COL_1+-COL_2-COL_2%COL_3) from T_VAR_POP_SAMP_VARIANCE01 order by 1;
select covar_samp(COL_1+COL_2-COL_2%COL_3,COL_1+COL_2-COL_2%COL_3) from T_VAR_POP_SAMP_VARIANCE01 order by 1;
drop table if exists T_VAR_POP_SAMP_VARIANCE01;